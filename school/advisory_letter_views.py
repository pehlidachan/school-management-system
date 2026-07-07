from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .access_control import admin_required
from .models import Grade, Student


LETTER_TYPES = {
    "general": {
        "title": "Student Advisory Letter",
        "subject": "Student Conduct Advisory",
        "body": "The school has observed that the student named below requires improvement in conduct, discipline, punctuality, homework completion, or general academic attitude.",
    },
    "attendance": {
        "title": "Attendance Advisory Letter",
        "subject": "Attendance / Punctuality Advisory",
        "body": "The school record indicates that attendance or punctuality needs improvement. Regular attendance is compulsory for academic progress.",
    },
    "dues": {
        "title": "Fee Reminder Letter",
        "subject": "School Office Reminder",
        "body": "The parent or guardian is requested to contact the school office regarding student record and any pending office matters after verification.",
    },
    "performance": {
        "title": "Performance Advisory Letter",
        "subject": "Academic Performance Advisory",
        "body": "The school has observed that academic performance needs improvement. Parents are requested to guide the student and remain in contact with the class teacher.",
    },
}


def _letter_meta(letter_type):
    return LETTER_TYPES.get(letter_type, LETTER_TYPES["general"])


@admin_required
def student_advisory_letter(request, student_id, letter_type="general"):
    student = get_object_or_404(Student.objects.select_related("grade", "gender", "guardian_relation"), id=student_id)
    letter = _letter_meta(letter_type)
    return render(request, "print/student_advisory_letter.html", {
        "students": [student],
        "letter": letter,
        "letter_type": letter_type,
        "letter_types": LETTER_TYPES,
        "print_date": timezone.localdate(),
        "is_bulk": False,
        "title": letter["title"],
    })


@admin_required
def bulk_student_advisory_letters(request):
    grades = Grade.objects.filter(status=True).order_by("name")
    grade_id = request.GET.get("grade") or ""
    letter_type = request.GET.get("type") or "general"
    letter = _letter_meta(letter_type)
    selected_grade = None
    students = Student.objects.none()

    if grade_id:
        selected_grade = get_object_or_404(Grade, id=grade_id)
        students = Student.objects.filter(grade=selected_grade, status=True).select_related(
            "grade", "gender", "guardian_relation"
        ).order_by("name")

    return render(request, "print/student_advisory_letter.html", {
        "grades": grades,
        "selected_grade": selected_grade,
        "selected_grade_id": str(grade_id),
        "students": students,
        "letter": letter,
        "letter_type": letter_type,
        "letter_types": LETTER_TYPES,
        "print_date": timezone.localdate(),
        "is_bulk": True,
        "title": f"Bulk {letter['title']}",
    })
