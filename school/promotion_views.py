from django.contrib import messages
from django.shortcuts import redirect, render

from .access_control import staff_required
from .models import Grade, Student


@staff_required
def student_promotion(request):
    grades = Grade.objects.filter(status=True).order_by("name")
    from_grade_id = request.GET.get("from_grade") or request.POST.get("from_grade")
    to_grade_id = request.POST.get("to_grade")
    students = Student.objects.none()
    from_grade = None

    if from_grade_id:
        try:
            from_grade = Grade.objects.get(id=from_grade_id, status=True)
            students = Student.objects.filter(grade=from_grade, status=True).order_by("name")
        except Grade.DoesNotExist:
            messages.error(request, "Selected class was not found.")
            return redirect("student_promotion")

    if request.method == "POST":
        selected_ids = request.POST.getlist("student_ids")
        if not from_grade_id or not to_grade_id:
            messages.error(request, "Please select both from class and promote to class.")
            return redirect("student_promotion")
        if from_grade_id == to_grade_id:
            messages.error(request, "From class and promote-to class cannot be same.")
            return redirect(f"/students/promotion/?from_grade={from_grade_id}")
        if not selected_ids:
            messages.error(request, "Please select at least one student to promote.")
            return redirect(f"/students/promotion/?from_grade={from_grade_id}")

        to_grade = Grade.objects.get(id=to_grade_id, status=True)
        promoted_count = Student.objects.filter(id__in=selected_ids, grade_id=from_grade_id, status=True).update(grade=to_grade)
        messages.success(request, f"{promoted_count} student(s) promoted successfully to {to_grade}.")
        return redirect(f"/students/promotion/?from_grade={to_grade.id}")

    return render(request, "student_promotion.html", {
        "grades": grades,
        "students": students,
        "from_grade": from_grade,
        "from_grade_id": str(from_grade_id or ""),
    })
