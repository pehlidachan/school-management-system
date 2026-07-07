from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .access_control import admin_required
from .models import Grade, Student


CERTIFICATE_TYPES = {
    "character": {
        "title": "Character Certificate",
        "heading": "Certificate of Character",
        "body": "This is to certify that the student named below has remained enrolled in this institution. During the period known to the school, the student's conduct and character have been found satisfactory.",
        "purpose": "Issued on request for official use.",
    },
    "hope": {
        "title": "Hope Certificate",
        "heading": "Hope Certificate",
        "body": "This is to certify that the student named below is expected to appear / continue studies with good academic conduct. The school wishes the student success in future educational progress.",
        "purpose": "Issued as a hope certificate for admission / examination / official record.",
    },
    "provisional": {
        "title": "Provisional Certificate",
        "heading": "Provisional Certificate",
        "body": "This is to certify provisionally that the student named below has been a bonafide student of this institution according to the available school record.",
        "purpose": "Issued provisionally until final verification / final record is completed.",
    },
    "leaving": {
        "title": "School Leaving Certificate",
        "heading": "School Leaving Certificate",
        "body": "This is to certify that the student named below has studied in this institution. The certificate is issued according to the available school record for onward admission / official use.",
        "purpose": "Issued for school leaving / transfer purpose.",
    },
    "appreciation": {
        "title": "Certificate of Appreciation",
        "heading": "Certificate of Appreciation",
        "body": "This certificate is proudly presented to the student named below in recognition of positive participation, discipline, and contribution to school learning activities.",
        "purpose": "Issued as appreciation by the school administration.",
    },
}


def _get_certificate(certificate_type):
    try:
        return CERTIFICATE_TYPES[certificate_type]
    except KeyError as exc:
        raise Http404("Certificate type not found") from exc


@admin_required
def student_certificate(request, student_id, certificate_type="character"):
    certificate = _get_certificate(certificate_type)
    student = get_object_or_404(
        Student.objects.select_related("grade", "gender", "guardian_relation"),
        id=student_id,
    )
    return render(request, "print/student_certificate.html", {
        "certificate": certificate,
        "certificate_type": certificate_type,
        "certificate_types": CERTIFICATE_TYPES,
        "students": [student],
        "print_date": timezone.localdate(),
        "is_bulk": False,
        "title": certificate["title"],
    })


@admin_required
def bulk_student_certificates(request):
    grades = Grade.objects.filter(status=True).order_by("name")
    grade_id = request.GET.get("grade") or ""
    certificate_type = request.GET.get("type") or "character"
    certificate = _get_certificate(certificate_type)
    selected_grade = None
    students = Student.objects.none()

    if grade_id:
        selected_grade = get_object_or_404(Grade, id=grade_id)
        students = Student.objects.filter(grade=selected_grade, status=True).select_related(
            "grade", "gender", "guardian_relation"
        ).order_by("name")

    return render(request, "print/student_certificate.html", {
        "grades": grades,
        "selected_grade": selected_grade,
        "selected_grade_id": str(grade_id),
        "certificate": certificate,
        "certificate_type": certificate_type,
        "certificate_types": CERTIFICATE_TYPES,
        "students": students,
        "print_date": timezone.localdate(),
        "is_bulk": True,
        "title": f"Bulk {certificate['title']}",
    })
