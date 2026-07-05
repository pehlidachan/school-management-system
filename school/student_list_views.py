from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render

from .access_control import admin_required, is_school_admin
from .models import Grade, Student


@admin_required
def display_students(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login first!")
        return redirect("login")
    if not is_school_admin(request.user):
        messages.warning(request, "This page is for admin only!")
        return redirect("home")

    query = (request.GET.get("q") or "").strip()
    grade_id = request.GET.get("grade") or ""
    status = request.GET.get("status") or ""

    students = Student.objects.select_related("grade", "gender", "guardian_relation").order_by("name")
    if query:
        search_filter = Q(name__icontains=query) | Q(guardian_name__icontains=query) | Q(phone__icontains=query) | Q(emergency_phone__icontains=query)
        if query.isdigit():
            search_filter |= Q(id=int(query))
        students = students.filter(search_filter)
    if grade_id:
        students = students.filter(grade_id=grade_id)
    if status == "active":
        students = students.filter(status=True)
    elif status == "inactive":
        students = students.filter(status=False)

    data = list(students[:300])
    context = {
        "data": data,
        "grades": Grade.objects.filter(status=True).order_by("name"),
        "q": query,
        "selected_grade_id": str(grade_id),
        "selected_status": status,
        "result_count": len(data),
    }
    return render(request, "display_students.html", context)
