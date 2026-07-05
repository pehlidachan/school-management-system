from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access_control import staff_required
from .exam_models import Exam, ExamSubject, StudentMark
from .models import Grade, Student, Subject


def _date_or_none(value):
    if not value:
        return None
    try:
        return timezone.datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _decimal(value, default="0"):
    try:
        return Decimal(str(value or default))
    except (InvalidOperation, ValueError):
        return Decimal(default)


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
        })
    return result_rows, exam_subjects


@staff_required
def exam_dashboard(request):
    exams = Exam.objects.select_related("grade", "created_by").annotate(subject_count=Count("exam_subjects"))[:50]
    context = {
        "exams": exams,
        "total_exams": Exam.objects.count(),
        "published_exams": Exam.objects.filter(is_published=True).count(),
        "total_marks": StudentMark.objects.count(),
    }
    return render(request, "exam_dashboard.html", context)


@staff_required
def add_exam(request):
    grades = Grade.objects.filter(status=True).order_by("name")
    if request.method == "POST":
        grade = get_object_or_404(Grade, id=request.POST.get("grade"))
        name = (request.POST.get("name") or "").strip()
        if not name:
            messages.error(request, "Exam name is required.")
            return redirect("add_exam")
        Exam.objects.create(
            name=name,
            grade=grade,
            start_date=_date_or_none(request.POST.get("start_date")) or timezone.localdate(),
            end_date=_date_or_none(request.POST.get("end_date")),
            is_published=bool(request.POST.get("is_published")),
            created_by=request.user,
        )
        messages.success(request, "Exam created successfully.")
        return redirect("exam_dashboard")
    return render(request, "exam_form.html", {"grades": grades, "today": timezone.localdate()})


@staff_required
def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam.objects.select_related("grade"), id=exam_id)
    exam_subjects = exam.exam_subjects.select_related("subject")
    return render(request, "exam_detail.html", {"exam": exam, "exam_subjects": exam_subjects})


@staff_required
def add_exam_subject(request, exam_id):
    exam = get_object_or_404(Exam.objects.select_related("grade"), id=exam_id)
    subjects = Subject.objects.order_by("name")
    if request.method == "POST":
        subject = get_object_or_404(Subject, id=request.POST.get("subject"))
        ExamSubject.objects.update_or_create(
            exam=exam,
            subject=subject,
            defaults={
                "total_marks": _decimal(request.POST.get("total_marks"), "100"),
                "passing_marks": _decimal(request.POST.get("passing_marks"), "33"),
            },
        )
        messages.success(request, "Subject added to exam.")
        return redirect("exam_detail", exam_id=exam.id)
    return render(request, "exam_subject_form.html", {"exam": exam, "subjects": subjects})


@staff_required
def marks_entry(request, exam_subject_id):
    exam_subject = get_object_or_404(ExamSubject.objects.select_related("exam", "exam__grade", "subject"), id=exam_subject_id)
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
    exam = get_object_or_404(Exam.objects.select_related("grade"), id=exam_id)
    result_rows, exam_subjects = _build_result_rows(exam)
    return render(request, "exam_results.html", {"exam": exam, "result_rows": result_rows, "exam_subjects": exam_subjects})


@staff_required
def student_result_card(request, exam_id, student_id):
    exam = get_object_or_404(Exam.objects.select_related("grade"), id=exam_id)
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
