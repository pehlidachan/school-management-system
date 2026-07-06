from datetime import datetime

from django.contrib import messages
from django.shortcuts import redirect, render

from .public_models import JobApplication, OnlineAdmissionApplication, ParentComplaint


def _date_or_none(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _clean(request, key):
    return (request.POST.get(key) or "").strip()


def _spam_detected(request):
    return bool((request.POST.get("website") or "").strip())


def _valid_phone(value):
    digits = ''.join(ch for ch in value if ch.isdigit())
    return len(digits) >= 7


def public_success(request):
    return render(request, "public_success.html")


def parent_complaint_form(request):
    if request.method == "POST":
        if _spam_detected(request):
            return redirect("public_success")
        parent_name = _clean(request, "parent_name")
        student_name = _clean(request, "student_name")
        phone = _clean(request, "phone")
        subject = _clean(request, "subject")
        message = _clean(request, "message")
        if not parent_name or not student_name or not phone or not subject or not message:
            messages.error(request, "Please fill all required fields.")
            return redirect("parent_complaint_form")
        if not _valid_phone(phone):
            messages.error(request, "Please enter a valid phone number.")
            return redirect("parent_complaint_form")
        ParentComplaint.objects.create(
            parent_name=parent_name,
            student_name=student_name,
            student_class=_clean(request, "student_class"),
            phone=phone,
            email=_clean(request, "email"),
            subject=subject,
            message=message,
        )
        messages.success(request, "Request submitted successfully.")
        return redirect("public_success")
    return render(request, "public_parent_complaint.html")


def online_admission_form(request):
    if request.method == "POST":
        if _spam_detected(request):
            return redirect("public_success")
        student_name = _clean(request, "student_name")
        desired_class = _clean(request, "desired_class")
        father_name = _clean(request, "father_name")
        guardian_phone = _clean(request, "guardian_phone")
        address = _clean(request, "address")
        if not student_name or not desired_class or not father_name or not guardian_phone or not address:
            messages.error(request, "Please fill all required fields.")
            return redirect("online_admission_form")
        if not _valid_phone(guardian_phone):
            messages.error(request, "Please enter a valid phone number.")
            return redirect("online_admission_form")
        OnlineAdmissionApplication.objects.create(
            student_name=student_name,
            desired_class=desired_class,
            dob=_date_or_none(request.POST.get("dob")),
            gender=_clean(request, "gender"),
            father_name=father_name,
            guardian_phone=guardian_phone,
            guardian_email=_clean(request, "guardian_email"),
            previous_school=_clean(request, "previous_school"),
            address=address,
            note=_clean(request, "note"),
        )
        messages.success(request, "Request submitted successfully.")
        return redirect("public_success")
    return render(request, "public_admission_form.html")


def job_apply_form(request):
    if request.method == "POST":
        if _spam_detected(request):
            return redirect("public_success")
        applicant_name = _clean(request, "applicant_name")
        applied_for = _clean(request, "applied_for")
        qualification = _clean(request, "qualification")
        phone = _clean(request, "phone")
        if not applicant_name or not applied_for or not qualification or not phone:
            messages.error(request, "Please fill all required fields.")
            return redirect("job_apply_form")
        if not _valid_phone(phone):
            messages.error(request, "Please enter a valid phone number.")
            return redirect("job_apply_form")
        JobApplication.objects.create(
            applicant_name=applicant_name,
            applied_for=applied_for,
            qualification=qualification,
            experience=_clean(request, "experience"),
            phone=phone,
            email=_clean(request, "email"),
            address=_clean(request, "address"),
            cover_note=_clean(request, "cover_note"),
        )
        messages.success(request, "Request submitted successfully.")
        return redirect("public_success")
    return render(request, "public_job_apply.html")
