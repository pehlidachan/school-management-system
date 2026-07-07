from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .access_control import admin_required
from .models import Grade, Student


@admin_required
def student_welcome_card(request, student_id):
    student = get_object_or_404(
        Student.objects.select_related("grade", "gender", "guardian_relation"),
        id=student_id,
    )
    return render(request, "print/student_welcome_card.html", {
        "students": [student],
        "print_date": timezone.localdate(),
        "title": f"Welcome Card - {student.name}",
        "is_bulk": False,
    })


@admin_required
def bulk_student_welcome_cards(request):
    grades = Grade.objects.filter(status=True).order_by("name")
    grade_id = request.GET.get("grade") or ""
    pending_only = request.GET.get("pending", "1") == "1"
    selected_grade = None
    students = Student.objects.none()

    if grade_id:
        selected_grade = get_object_or_404(Grade, id=grade_id)
        students = Student.objects.filter(grade=selected_grade, status=True).select_related(
            "grade", "gender", "guardian_relation"
        ).order_by("date_of_enrollment", "name")
        if pending_only:
            students = students.filter(welcome_card_sent=False)

    return render(request, "print/student_welcome_card.html", {
        "grades": grades,
        "selected_grade": selected_grade,
        "selected_grade_id": str(grade_id),
        "students": students,
        "pending_only": pending_only,
        "print_date": timezone.localdate(),
        "title": "Bulk Student Welcome Cards",
        "is_bulk": True,
    })


@admin_required
@require_POST
def mark_welcome_card_sent(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.welcome_card_sent = True
    student.save(update_fields=["welcome_card_sent"])
    messages.success(request, f"Welcome card marked as sent for {student.name}.")
    next_url = request.POST.get("next") or reverse("display_students")
    return redirect(next_url)


@admin_required
@require_POST
def reset_welcome_card_sent(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.welcome_card_sent = False
    student.save(update_fields=["welcome_card_sent"])
    messages.success(request, f"Welcome card status reset for {student.name}.")
    next_url = request.POST.get("next") or reverse("display_students")
    return redirect(next_url)
