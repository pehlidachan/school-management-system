from django.template.loader import render_to_string
from django.utils import timezone

from .exam_models import Exam


DEFAULT_SCHOOL_NAME = "PRODESK SMART SCHOOL"
DEFAULT_CAMPUS_CODE = "PSI"


def _brand_value(brand, field_name, default=""):
    return getattr(brand, field_name, None) or default


def get_student_class_label(student):
    academic_class = getattr(student, "academic_class", None)
    if academic_class:
        return academic_class.class_label or str(academic_class)
    grade = getattr(student, "grade", None)
    return str(grade) if grade else "-"


def get_student_parent_name(student):
    return getattr(student, "guardian_name", "") or getattr(student, "father_name", "") or "-"


def get_student_photo_url(student):
    photo_path = getattr(student, "photo_path", "") or ""
    if photo_path:
        return f"/{photo_path}"
    return ""


def get_marksheet_exam_list(student, only_published=True):
    queryset = Exam.objects.filter(grade=student.grade).select_related("scheme", "scheme_item", "grade")
    if only_published:
        queryset = queryset.filter(is_published=True)
    return queryset.order_by("sequence", "start_date", "id")


def build_marksheet_exams_list_context(student, exams=None, brand=None, request_date=None, reply_time=None, only_published=True):
    request_date = request_date or timezone.localdate()
    reply_time = reply_time or timezone.localtime()
    exams = list(exams if exams is not None else get_marksheet_exam_list(student, only_published=only_published))
    school_name = _brand_value(brand, "school_name", DEFAULT_SCHOOL_NAME)
    campus_code = _brand_value(brand, "campus_code", DEFAULT_CAMPUS_CODE)
    short_school_name = f"{school_name} ({campus_code})" if campus_code else school_name

    return {
        "student": student,
        "student_id_name": f"({student.id}) {student.name}",
        "class_label": get_student_class_label(student),
        "parent_name": get_student_parent_name(student),
        "student_photo_url": get_student_photo_url(student),
        "exams": exams,
        "request_date": request_date,
        "request_date_display": request_date.strftime("%a, %d-%b-%Y"),
        "reply_time": reply_time,
        "reply_time_display": reply_time.strftime("%-I:%M %p").lower() if hasattr(reply_time, "strftime") else "",
        "reply_title": "Marksheet Exams List",
        "section_label": "Exams List",
        "school_name": school_name,
        "campus_code": campus_code,
        "short_school_name": short_school_name,
        "brand": brand,
        "has_exams": bool(exams),
    }


def render_whatsapp_marksheet_exams_list(student, exams=None, brand=None, request_date=None, reply_time=None, only_published=True):
    context = build_marksheet_exams_list_context(
        student=student,
        exams=exams,
        brand=brand,
        request_date=request_date,
        reply_time=reply_time,
        only_published=only_published,
    )
    return render_to_string("replies/whatsapp/marksheet_exams_list.txt", context).strip()


def render_whatsapp_marksheet_exams_card_svg(student, exams=None, brand=None, request_date=None, reply_time=None, only_published=True):
    context = build_marksheet_exams_list_context(
        student=student,
        exams=exams,
        brand=brand,
        request_date=request_date,
        reply_time=reply_time,
        only_published=only_published,
    )
    return render_to_string("replies/whatsapp/marksheet_exams_list_card.svg", context).strip()


def render_email_marksheet_exams_list(student, exams=None, brand=None, request_date=None, reply_time=None, only_published=True):
    context = build_marksheet_exams_list_context(
        student=student,
        exams=exams,
        brand=brand,
        request_date=request_date,
        reply_time=reply_time,
        only_published=only_published,
    )
    return {
        "subject": render_to_string("replies/email/marksheet_exams_list_subject.txt", context).strip(),
        "text": render_to_string("replies/email/marksheet_exams_list.txt", context).strip(),
        "html": render_to_string("replies/email/marksheet_exams_list.html", context).strip(),
        "context": context,
    }
