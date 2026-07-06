from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .access_control import staff_required
from .models import Grade, Student


@staff_required
def class_register(request):
    grades = Grade.objects.filter(status=True).order_by('name')
    grade_id = request.GET.get('grade') or ''
    selected_grade = None
    students = Student.objects.none()
    if grade_id:
        selected_grade = get_object_or_404(Grade, id=grade_id, status=True)
        students = Student.objects.filter(grade=selected_grade, status=True).select_related('grade', 'gender', 'guardian_relation').order_by('name')
    return render(request, 'class_register.html', {
        'grades': grades,
        'selected_grade': selected_grade,
        'selected_grade_id': str(grade_id),
        'students': students,
        'print_date': timezone.localdate(),
    })
