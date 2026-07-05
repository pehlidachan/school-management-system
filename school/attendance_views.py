from datetime import datetime

from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access_control import staff_required
from .models import AttendanceSession, Grade, Student, StudentAttendance


STATUS_OPTIONS = StudentAttendance.STATUS_CHOICES


def _parse_date(value):
    if not value:
        return timezone.localdate()
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return timezone.localdate()


@staff_required
def attendance_dashboard(request):
    today = timezone.localdate()
    grades = Grade.objects.filter(status=True).order_by("name")
    recent_sessions = (
        AttendanceSession.objects.select_related("grade", "taken_by")
        .annotate(
            total=Count("records"),
            present=Count("records", filter=Q(records__status=StudentAttendance.PRESENT)),
            absent=Count("records", filter=Q(records__status=StudentAttendance.ABSENT)),
            late=Count("records", filter=Q(records__status=StudentAttendance.LATE)),
            leave=Count("records", filter=Q(records__status=StudentAttendance.LEAVE)),
        )[:10]
    )
    today_records = StudentAttendance.objects.filter(session__attendance_date=today)
    context = {
        "today": today,
        "grades": grades,
        "recent_sessions": recent_sessions,
        "total_students": Student.objects.filter(status=True).count(),
        "today_present": today_records.filter(status=StudentAttendance.PRESENT).count(),
        "today_absent": today_records.filter(status=StudentAttendance.ABSENT).count(),
        "today_late": today_records.filter(status=StudentAttendance.LATE).count(),
    }
    return render(request, "attendance_dashboard.html", context)


@staff_required
def mark_attendance(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    selected_date = _parse_date(request.POST.get("attendance_date") if request.method == "POST" else request.GET.get("date"))
    students = Student.objects.filter(grade=grade, status=True).order_by("name")

    if request.method == "POST":
        session, _ = AttendanceSession.objects.get_or_create(
            grade=grade,
            attendance_date=selected_date,
            defaults={"taken_by": request.user},
        )
        session.taken_by = request.user
        session.note = request.POST.get("note", "").strip()
        session.save(update_fields=["taken_by", "note", "updated_at"])

        for student in students:
            status = request.POST.get(f"status_{student.id}", StudentAttendance.PRESENT)
            if status not in dict(STATUS_OPTIONS):
                status = StudentAttendance.PRESENT
            remarks = request.POST.get(f"remarks_{student.id}", "").strip()[:255]
            StudentAttendance.objects.update_or_create(
                session=session,
                student=student,
                defaults={
                    "status": status,
                    "remarks": remarks,
                    "marked_by": request.user,
                },
            )

        messages.success(request, f"Attendance saved for {grade.name} on {selected_date}.")
        return redirect(f"/attendance/mark/{grade.id}/?date={selected_date}")

    session = AttendanceSession.objects.filter(grade=grade, attendance_date=selected_date).first()
    existing = {}
    if session:
        existing = {record.student_id: record for record in session.records.all()}

    rows = []
    for student in students:
        record = existing.get(student.id)
        rows.append({
            "student": student,
            "status": record.status if record else StudentAttendance.PRESENT,
            "remarks": record.remarks if record else "",
        })

    context = {
        "grade": grade,
        "selected_date": selected_date,
        "students": students,
        "rows": rows,
        "session": session,
        "status_options": STATUS_OPTIONS,
    }
    return render(request, "attendance_mark.html", context)


@staff_required
def attendance_report(request):
    sessions = (
        AttendanceSession.objects.select_related("grade", "taken_by")
        .annotate(
            total=Count("records"),
            present=Count("records", filter=Q(records__status=StudentAttendance.PRESENT)),
            absent=Count("records", filter=Q(records__status=StudentAttendance.ABSENT)),
            late=Count("records", filter=Q(records__status=StudentAttendance.LATE)),
            leave=Count("records", filter=Q(records__status=StudentAttendance.LEAVE)),
        )[:50]
    )
    return render(request, "attendance_report.html", {"sessions": sessions})


@staff_required
def attendance_session_detail(request, session_id):
    session = get_object_or_404(AttendanceSession.objects.select_related("grade", "taken_by"), id=session_id)
    records = session.records.select_related("student", "marked_by").order_by("student__name")
    return render(request, "attendance_session_detail.html", {"session": session, "records": records})
