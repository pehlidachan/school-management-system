from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .access_control import admin_required
from .models import Grade, Role, Staff, Student


@admin_required
def student_biodata_print(request, student_id):
    student = get_object_or_404(
        Student.objects.select_related("grade", "gender", "guardian_relation"),
        id=student_id,
    )
    return render(request, "print/student_biodata.html", {
        "students": [student],
        "print_date": timezone.localdate(),
        "title": f"Student Bio Data - {student.name}",
        "is_bulk": False,
    })


@admin_required
def bulk_student_biodata(request):
    grades = Grade.objects.filter(status=True).order_by("name")
    grade_id = request.GET.get("grade") or ""
    selected_grade = None
    students = Student.objects.none()

    if grade_id:
        selected_grade = get_object_or_404(Grade, id=grade_id)
        students = Student.objects.filter(grade=selected_grade).select_related(
            "grade", "gender", "guardian_relation"
        ).order_by("name")

    return render(request, "print/student_biodata.html", {
        "grades": grades,
        "selected_grade": selected_grade,
        "selected_grade_id": str(grade_id),
        "students": students,
        "print_date": timezone.localdate(),
        "title": "Bulk Student Bio Data",
        "is_bulk": True,
    })


@admin_required
def staff_biodata_print(request, staff_id):
    staff = get_object_or_404(
        Staff.objects.select_related("role", "subject", "gender", "employment_status"),
        id=staff_id,
    )
    return render(request, "print/staff_biodata.html", {
        "staff_members": [staff],
        "print_date": timezone.localdate(),
        "title": f"Staff Bio Data - {staff.name}",
        "is_bulk": False,
    })


@admin_required
def bulk_staff_biodata(request):
    roles = Role.objects.order_by("name")
    role_id = request.GET.get("role") or ""
    selected_role = None
    staff_members = Staff.objects.none()

    if role_id:
        selected_role = get_object_or_404(Role, id=role_id)
        staff_members = Staff.objects.filter(role=selected_role).select_related(
            "role", "subject", "gender", "employment_status"
        ).order_by("name")

    return render(request, "print/staff_biodata.html", {
        "roles": roles,
        "selected_role": selected_role,
        "selected_role_id": str(role_id),
        "staff_members": staff_members,
        "print_date": timezone.localdate(),
        "title": "Bulk Staff Bio Data",
        "is_bulk": True,
    })
