from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .access_control import staff_required
from .models import Grade, Student


@staff_required
def student_id_card(request, student_id):
    student = get_object_or_404(
        Student.objects.select_related("grade", "gender", "guardian_relation"),
        id=student_id,
    )
    return render(request, "student_id_card.html", {
        "student": student,
        "print_date": timezone.localdate(),
    })


@staff_required
def bulk_student_id_cards(request):
    grades = Grade.objects.filter(status=True).order_by("name")
    grade_id = request.GET.get("grade")
    selected_grade = None
    students = Student.objects.none()
    if grade_id:
        selected_grade = get_object_or_404(Grade, id=grade_id, status=True)
        students = Student.objects.filter(grade=selected_grade, status=True).select_related("grade", "gender", "guardian_relation").order_by("name")
    return render(request, "bulk_student_id_cards.html", {
        "grades": grades,
        "selected_grade": selected_grade,
        "selected_grade_id": str(grade_id or ""),
        "students": students,
        "print_date": timezone.localdate(),
    })
