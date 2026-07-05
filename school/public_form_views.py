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


def parent_complaint_form(request):
    if request.method == "POST":
        ParentComplaint.objects.create(
            parent_name=(request.POST.get("parent_name") or "").strip(),
            student_name=(request.POST.get("student_name") or "").strip(),
            student_class=(request.POST.get("student_class") or "").strip(),
            phone=(request.POST.get("phone") or "").strip(),
            email=(request.POST.get("email") or "").strip(),
            subject=(request.POST.get("subject") or "").strip(),
            message=(request.POST.get("message") or "").strip(),
        )
        messages.success(request, "Complaint submitted successfully.")
        return redirect("home")
    return render(request, "public_parent_complaint.html")


def online_admission_form(request):
    if request.method == "POST":
        OnlineAdmissionApplication.objects.create(
            student_name=(request.POST.get("student_name") or "").strip(),
            desired_class=(request.POST.get("desired_class") or "").strip(),
            dob=_date_or_none(request.POST.get("dob")),
            gender=(request.POST.get("gender") or "").strip(),
            father_name=(request.POST.get("father_name") or "").strip(),
            guardian_phone=(request.POST.get("guardian_phone") or "").strip(),
            guardian_email=(request.POST.get("guardian_email") or "").strip(),
            previous_school=(request.POST.get("previous_school") or "").strip(),
            address=(request.POST.get("address") or "").strip(),
            note=(request.POST.get("note") or "").strip(),
        )
        messages.success(request, "Admission application submitted successfully.")
        return redirect("home")
    return render(request, "public_admission_form.html")


def job_apply_form(request):
    if request.method == "POST":
        JobApplication.objects.create(
            applicant_name=(request.POST.get("applicant_name") or "").strip(),
            applied_for=(request.POST.get("applied_for") or "").strip(),
            qualification=(request.POST.get("qualification") or "").strip(),
            experience=(request.POST.get("experience") or "").strip(),
            phone=(request.POST.get("phone") or "").strip(),
            email=(request.POST.get("email") or "").strip(),
            address=(request.POST.get("address") or "").strip(),
            cover_note=(request.POST.get("cover_note") or "").strip(),
        )
        messages.success(request, "Job application submitted successfully.")
        return redirect("home")
    return render(request, "public_job_apply.html")
