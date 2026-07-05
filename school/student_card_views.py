from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .access_control import staff_required
from .models import Student


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
