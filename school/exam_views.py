from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access_control import staff_required
from .exam_models import Exam, ExamDateSheetItem, ExamScheme, ExamSchemeItem, ExamSubject, StudentMark
from .models import Grade, Student, Subject


def _date_or_none(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _decimal(value, default="0"):
    try:
        return Decimal(str(value or default))
    except (InvalidOperation, ValueError):
        return Decimal(default)


def _default_academic_year():
    today = timezone.localdate()
    return str(today.year)


def _get_default_scheme():
    return ExamScheme.objects.filter(is_default=True, is_active=True).first() or ExamScheme.objects.filter(is_active=True).first()


def _build_result_rows(exam, students=None):
    if students is None:
        students = Student.objects.filter(grade=exam.grade, status=True).order_by("name")
    exam_subjects = list(exam.exam_subjects.select_related("subject"))
    mark_map = {(m.student_id, m.exam_subject_id): m for m in StudentMark.objects.filter(exam_subject__exam=exam)}

    result_rows = []
    for student in students:
        obtained = Decimal("0")
        total = Decimal("0")
        failed = False
        subject_rows = []
        for exam_subject in exam_subjects:
            total += exam_subject.total_marks
            mark = mark_map.get((student.id, exam_subject.id))
            marks_obtained = mark.marks_obtained if mark else Decimal("0")
            obtained += marks_obtained
            if marks_obtained < exam_subject.passing_marks:
                failed = True
            subject_rows.append({
                "subject": exam_subject.subject,
                "marks": marks_obtained,
                "total": exam_subject.total_marks,
                "passing": exam_subject.passing_marks,
                "status": "Pass" if marks_obtained >= exam_subject.passing_marks else "Fail",
            })
        percentage = (obtained / total * 100) if total else Decimal("0")
        result_rows.append({
            "student": student,
            "obtained": obtained,
            "total": total,
            "percentage": percentage.quantize(Decimal("0.01")) if total else Decimal("0"),
            "status": "Fail" if failed else "Pass",
            "subjects": subject_rows,
            "exam_weight": exam.result_weight,
            "weighted_score": (percentage * exam.result_weight / Decimal("100")).quantize(Decimal("0.01")) if total else Decimal("0"),
        })
    return result_rows, exam_subjects


def _ensure_datesheet_items(exam):
    start = exam.start_date or timezone.localdate()
    exam_subjects = list(exam.exam_subjects.select_related("subject").order_by("subject__name"))
    for index, item in enumerate(exam_subjects):
        ExamDateSheetItem.objects.get_or_create(
            exam_subject=item,
            defaults={
                "paper_date": start + timedelta(days=index),
                "sort_order": index + 1,
                "start_time": "09:00",
                "end_time": "12:00",
            },
        )


def _build_datesheet_rows(exam):
    _ensure_datesheet_items(exam)
    rows = []
    items = ExamDateSheetItem.objects.filter(exam_subject__exam=exam).select_related("exam_subject", "exam_subject__subject")
    for index, item in enumerate(items, start=1):
        rows.append({
            "serial": index,
            "date": item.paper_date,
            "day": item.paper_date.strftime("%A"),
            "subject": item.exam_subject.subject,
            "total_marks": item.exam_subject.total_marks,
            "passing_marks": item.exam_subject.passing_marks,
            "time": f"{item.start_time.strftime('%I:%M %p')} - {item.end_time.strftime('%I:%M %p')}",
            "room": item.room,
            "instructions": item.instructions,
        })
    return rows


@staff_required
def exam_dashboard(request):
    exams = Exam.objects.select_related("grade", "created_by", "scheme", "scheme_item").annotate(subject_count=Count("exam_subjects"))[:50]
    context = {
        "exams": exams,
        "schemes": ExamScheme.objects.prefetch_related("items").all(),
        "total_schemes": ExamScheme.objects.count(),
        "total_exams": Exam.objects.count(),
        "published_exams": Exam.objects.filter(is_published=True).count(),
        "locked_exams": Exam.objects.filter(is_locked=True).count(),
        "total_marks": StudentMark.objects.count(),
        "exam_types": Exam.EXAM_TYPE_CHOICES,
    }
    return render(request, "exam_dashboard.html", context)


@staff_required
def add_exam(request):
    grades = Grade.objects.filter(status=True).order_by("name")
    schemes = ExamScheme.objects.filter(is_active=True).prefetch_related("items").order_by("-is_default", "name")
    default_scheme = _get_default_scheme()
    if request.method == "POST":
        grade = get_object_or_404(Grade, id=request.POST.get("grade"))
        scheme = get_object_or_404(ExamScheme, id=request.POST.get("scheme")) if request.POST.get("scheme") else default_scheme
        scheme_item = get_object_or_404(ExamSchemeItem, id=request.POST.get("scheme_item"), scheme=scheme) if request.POST.get("scheme_item") else None
        exam_type = scheme_item.item_key if scheme_item else (request.POST.get("exam_type") or Exam.MONTHLY_TEST)
        name = (request.POST.get("name") or "").strip()
        if not name:
            name = scheme_item.display_name if scheme_item else dict(Exam.EXAM_TYPE_CHOICES).get(exam_type, "Monthly Test")
        exam = Exam.objects.create(
            scheme=scheme,
            scheme_item=scheme_item,
            name=name,
            exam_type=exam_type,
            academic_year=(request.POST.get("academic_year") or _default_academic_year()).strip(),
            term_label=(request.POST.get("term_label") or "").strip(),
            grade=grade,
            start_date=_date_or_none(request.POST.get("start_date")) or timezone.localdate(),
            end_date=_date_or_none(request.POST.get("end_date")),
            sequence=int(request.POST.get("sequence") or (scheme_item.sequence if scheme_item else Exam.EXAM_SEQUENCE.get(exam_type, 20))),
            result_weight=_decimal(request.POST.get("result_weight"), str(scheme_item.result_weight if scheme_item else Exam.DEFAULT_WEIGHT.get(exam_type, Decimal("10.00")))),
            is_published=bool(request.POST.get("is_published")),
            is_locked=bool(request.POST.get("is_locked")),
            created_by=request.user,
        )
        messages.success(request, f"{exam.name} created from {scheme.name if scheme else 'manual schema'}.")
        return redirect("exam_dashboard")
    return render(request, "exam_form.html", {
        "grades": grades,
        "schemes": schemes,
        "default_scheme": default_scheme,
        "today": timezone.localdate(),
        "academic_year": _default_academic_year(),
        "exam_types": Exam.EXAM_TYPE_CHOICES,
        "default_sequence": 20,
        "default_weight": "10.00",
    })


@staff_required
def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam.objects.select_related("grade", "scheme", "scheme_item"), id=exam_id)
    exam_subjects = exam.exam_subjects.select_related("subject")
    return render(request, "exam_detail.html", {"exam": exam, "exam_subjects": exam_subjects})


@staff_required
def add_exam_subject(request, exam_id):
    exam = get_object_or_404(Exam.objects.select_related("grade", "scheme_item"), id=exam_id)
    if exam.is_locked:
        messages.error(request, "This exam is locked. Unlock it before changing subjects.")
        return redirect("exam_detail", exam_id=exam.id)
    subjects = Subject.objects.order_by("name")
    if request.method == "POST":
        subject = get_object_or_404(Subject, id=request.POST.get("subject"))
        total_default = str(exam.scheme_item.default_total_marks) if exam.scheme_item else "100"
        passing_default = str(exam.scheme_item.default_passing_marks) if exam.scheme_item else "33"
        exam_subject, _ = ExamSubject.objects.update_or_create(
            exam=exam,
            subject=subject,
            defaults={
                "total_marks": _decimal(request.POST.get("total_marks"), total_default),
                "passing_marks": _decimal(request.POST.get("passing_marks"), passing_default),
            },
        )
        ExamDateSheetItem.objects.get_or_create(
            exam_subject=exam_subject,
            defaults={"paper_date": exam.start_date, "sort_order": exam.exam_subjects.count()},
        )
        messages.success(request, "Subject added to exam schema.")
        return redirect("exam_detail", exam_id=exam.id)
    return render(request, "exam_subject_form.html", {"exam": exam, "subjects": subjects})


@staff_required
def marks_entry(request, exam_subject_id):
    exam_subject = get_object_or_404(ExamSubject.objects.select_related("exam", "exam__grade", "subject"), id=exam_subject_id)
    if exam_subject.exam.is_locked:
        messages.error(request, "This exam is locked. Marks cannot be changed.")
        return redirect("exam_detail", exam_id=exam_subject.exam.id)
    students = Student.objects.filter(grade=exam_subject.exam.grade, status=True).order_by("name")
    existing = {item.student_id: item for item in StudentMark.objects.filter(exam_subject=exam_subject)}

    if request.method == "POST":
        for student in students:
            marks = _decimal(request.POST.get(f"marks_{student.id}"), "0")
            remarks = (request.POST.get(f"remarks_{student.id}") or "").strip()[:255]
            StudentMark.objects.update_or_create(
                exam_subject=exam_subject,
                student=student,
                defaults={"marks_obtained": marks, "remarks": remarks, "marked_by": request.user},
            )
        messages.success(request, "Marks saved successfully.")
        return redirect("marks_entry", exam_subject_id=exam_subject.id)

    rows = []
    for student in students:
        mark = existing.get(student.id)
        rows.append({"student": student, "mark": mark})
    return render(request, "marks_entry.html", {"exam_subject": exam_subject, "rows": rows})


@staff_required
def exam_results(request, exam_id):
    exam = get_object_or_404(Exam.objects.select_related("grade", "scheme", "scheme_item"), id=exam_id)
    result_rows, exam_subjects = _build_result_rows(exam)
    return render(request, "exam_results.html", {"exam": exam, "result_rows": result_rows, "exam_subjects": exam_subjects})


@staff_required
def exam_datesheet(request, exam_id):
    exam = get_object_or_404(Exam.objects.select_related("grade", "scheme", "scheme_item"), id=exam_id)
    rows = _build_datesheet_rows(exam)
    return render(request, "exam_datesheet.html", {
        "exam": exam,
        "rows": rows,
        "print_date": timezone.localdate(),
    })


@staff_required
def student_result_card(request, exam_id, student_id):
    exam = get_object_or_404(Exam.objects.select_related("grade", "scheme", "scheme_item"), id=exam_id)
    student = get_object_or_404(Student.objects.select_related("grade", "gender", "guardian_relation"), id=student_id, grade=exam.grade)
    result_rows, exam_subjects = _build_result_rows(exam, students=[student])
    result = result_rows[0] if result_rows else None
    return render(request, "student_result_card.html", {
        "exam": exam,
        "student": student,
        "result": result,
        "exam_subjects": exam_subjects,
        "print_date": timezone.localdate(),
    })


@staff_required
def bulk_result_cards(request, exam_id):
    exam = get_object_or_404(Exam.objects.select_related("grade", "scheme", "scheme_item"), id=exam_id)
    result_rows, exam_subjects = _build_result_rows(exam)
    return render(request, "bulk_result_cards.html", {
        "exam": exam,
        "result_rows": result_rows,
        "exam_subjects": exam_subjects,
        "print_date": timezone.localdate(),
    })
