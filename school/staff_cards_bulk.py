from django.shortcuts import render
from django.utils import timezone

from .access_control import admin_required
from .models import EmploymentStatus, Role, Staff


@admin_required
def bulk_cards(request):
    role_id = request.GET.get('role') or ''
    emp_id = request.GET.get('employment_status') or ''
    view_status = request.GET.get('status') or 'active'
    qs = Staff.objects.select_related('role', 'subject', 'gender', 'employment_status').order_by('name')
    if role_id:
        qs = qs.filter(role_id=role_id)
    if emp_id:
        qs = qs.filter(employment_status_id=emp_id)
    if view_status == 'active':
        qs = qs.filter(status=True)
    if view_status == 'inactive':
        qs = qs.filter(status=False)
    records = list(qs[:300])
    return render(request, 'bulk_staff_id_cards.html', {
        'staff_list': records,
        'roles': Role.objects.order_by('name'),
        'employment_statuses': EmploymentStatus.objects.order_by('name'),
        'selected_role_id': str(role_id),
        'selected_employment_status_id': str(emp_id),
        'selected_status': view_status,
        'result_count': len(records),
        'print_date': timezone.localdate(),
    })
