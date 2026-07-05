from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render

from .access_control import admin_required, is_school_admin
from .models import EmploymentStatus, Role, Staff


@admin_required
def display_staff(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login first!")
        return redirect("login")
    if not is_school_admin(request.user):
        messages.warning(request, "This page is for admin only!")
        return redirect("home")

    query = (request.GET.get("q") or "").strip()
    role_id = request.GET.get("role") or ""
    employment_status_id = request.GET.get("employment_status") or ""
    status = request.GET.get("status") or ""

    staff = Staff.objects.select_related("role", "subject", "gender", "employment_status").order_by("name")
    if query:
        search_filter = Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query) | Q(qualification__icontains=query)
        if query.isdigit():
            search_filter |= Q(id=int(query))
        staff = staff.filter(search_filter)
    if role_id:
        staff = staff.filter(role_id=role_id)
    if employment_status_id:
        staff = staff.filter(employment_status_id=employment_status_id)
    if status == "active":
        staff = staff.filter(status=True)
    elif status == "inactive":
        staff = staff.filter(status=False)

    staff_list = list(staff[:300])
    context = {
        "staff": staff_list,
        "roles": Role.objects.order_by("name"),
        "employment_statuses": EmploymentStatus.objects.order_by("name"),
        "q": query,
        "selected_role_id": str(role_id),
        "selected_employment_status_id": str(employment_status_id),
        "selected_status": status,
        "result_count": len(staff_list),
    }
    return render(request, "staff_filtered_list_v2.html", context)
