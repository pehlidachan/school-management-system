from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access_control import staff_required
from .models import Grade, Subject
from .study_material_models import StudyMaterial


@staff_required
def study_material_center(request):
    grades = Grade.objects.filter(status=True).order_by("name")
    subjects = Subject.objects.order_by("name")
    grade_id = request.GET.get("grade") or ""
    subject_id = request.GET.get("subject") or ""
    q = (request.GET.get("q") or "").strip()

    materials = StudyMaterial.objects.select_related("grade", "subject", "created_by")
    if grade_id:
        materials = materials.filter(grade_id=grade_id)
    if subject_id:
        materials = materials.filter(subject_id=subject_id)
    if q:
        materials = materials.filter(title__icontains=q)

    return render(request, "study_material_center.html", {
        "materials": materials[:200],
        "grades": grades,
        "subjects": subjects,
        "selected_grade_id": str(grade_id),
        "selected_subject_id": str(subject_id),
        "q": q,
    })


@staff_required
def add_study_material(request):
    grades = Grade.objects.filter(status=True).order_by("name")
    subjects = Subject.objects.order_by("name")
    if request.method == "POST":
        grade_id = request.POST.get("grade") or None
        subject_id = request.POST.get("subject") or None
        StudyMaterial.objects.create(
            title=(request.POST.get("title") or "Study Material").strip(),
            grade_id=grade_id,
            subject_id=subject_id,
            description=(request.POST.get("description") or "").strip(),
            content=(request.POST.get("content") or "").strip(),
            external_url=(request.POST.get("external_url") or "").strip(),
            is_published=bool(request.POST.get("is_published")),
            created_by=request.user,
        )
        messages.success(request, "Study material added successfully.")
        return redirect("study_material_center")
    return render(request, "study_material_form.html", {"grades": grades, "subjects": subjects})


@staff_required
def study_material_detail(request, material_id):
    material = get_object_or_404(StudyMaterial.objects.select_related("grade", "subject", "created_by"), id=material_id)
    share_text = "\n".join([
        "Study Material",
        f"Title: {material.title}",
        f"Class: {material.grade or '-'}",
        f"Subject: {material.subject or '-'}",
        f"Link: {material.external_url or 'Available from school ERP'}",
        "Government Middle School Shalgah",
    ])
    return render(request, "study_material_detail.html", {"material": material, "share_text": share_text, "print_date": timezone.localdate()})
