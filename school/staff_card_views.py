from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .access_control import admin_required
from .models import Staff


@admin_required
def staff_id_card(request, staff_id):
    staff = get_object_or_404(
        Staff.objects.select_related("role", "subject", "gender", "employment_status"),
        id=staff_id,
    )
    return render(request, "staff_id_card.html", {
        "staff": staff,
        "print_date": timezone.localdate(),
    })
