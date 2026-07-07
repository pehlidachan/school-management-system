from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access_control import staff_required
from .models import Staff
from .staff_attendance_models import StaffLectureAttendance, StaffLectureSession


@staff_required
def staff_attendance_dashboard(request):
    sessions = StaffLectureSession.objects.select_related("taken_by").annotate(record_count=Count("records"))[:50]
    return render(request, "staff_attendance_dashboard.html", {"sessions": sessions, "today": timezone.localdate()})


@staff_required
def create_staff_attendance_session(request):
    if request.method == "POST":
        session = StaffLectureSession.objects.create(
            session_date=request.POST.get("session_date") or timezone.localdate(),
            title=(request.POST.get("title") or "Daily Staff Lecture Attendance").strip(),
            note=(request.POST.get("note") or "").strip(),
            taken_by=request.user,
        )
        messages.success(request, "Staff lecture attendance session created.")
        return redirect("mark_staff_attendance", session_id=session.id)
    return render(request, "staff_attendance_session_form.html", {"today": timezone.localdate()})


@staff_required
def mark_staff_attendance(request, session_id):
    session = get_object_or_404(StaffLectureSession, id=session_id)
    staff_members = Staff.objects.filter(status=True).select_related("role", "subject").order_by("name")
    existing = {item.staff_id: item for item in StaffLectureAttendance.objects.filter(session=session)}

    if request.method == "POST":
        for member in staff_members:
            StaffLectureAttendance.objects.update_or_create(
                session=session,
                staff=member,
                defaults={
                    "status": request.POST.get(f"status_{member.id}") or StaffLectureAttendance.PRESENT,
                    "lecture_title": (request.POST.get(f"lecture_{member.id}") or session.title).strip()[:160],
                    "remarks": (request.POST.get(f"remarks_{member.id}") or "").strip()[:255],
                    "marked_by": request.user,
                },
            )
        messages.success(request, "Staff lecture attendance saved.")
        return redirect("staff_attendance_detail", session_id=session.id)

    rows = []
    for member in staff_members:
        rows.append({"member": member, "record": existing.get(member.id)})
    return render(request, "mark_staff_attendance.html", {"session": session, "rows": rows, "status_choices": StaffLectureAttendance.STATUS_CHOICES})


@staff_required
def staff_attendance_detail(request, session_id):
    session = get_object_or_404(StaffLectureSession.objects.select_related("taken_by"), id=session_id)
    records = session.records.select_related("staff", "staff__role", "staff__subject", "marked_by").order_by("staff__name")
    summary = records.values("status").annotate(total=Count("id"))
    return render(request, "staff_attendance_detail.html", {"session": session, "records": records, "summary": summary, "print_date": timezone.localdate()})
