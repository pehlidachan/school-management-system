from datetime import datetime

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access_control import staff_required
from .gatepass_models import GatePass
from .models import Staff, Student


def _datetime_or_none(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M')
    except ValueError:
        return None


@staff_required
def gatepass_dashboard(request):
    status = request.GET.get('status') or ''
    records = GatePass.objects.select_related('student', 'staff', 'issued_by')
    if status:
        records = records.filter(status=status)
    return render(request, 'gatepass_dashboard.html', {
        'records': records[:300],
        'selected_status': status,
        'total_records': GatePass.objects.count(),
    })


@staff_required
def add_gatepass(request):
    students = Student.objects.filter(status=True).order_by('name')
    staff_members = Staff.objects.filter(status=True).order_by('name')
    if request.method == 'POST':
        person_type = request.POST.get('person_type') or GatePass.PERSON_STUDENT
        student = None
        staff = None
        if person_type == GatePass.PERSON_STUDENT and request.POST.get('student'):
            student = Student.objects.filter(id=request.POST.get('student')).first()
        if person_type == GatePass.PERSON_STAFF and request.POST.get('staff'):
            staff = Staff.objects.filter(id=request.POST.get('staff')).first()
        record = GatePass.objects.create(
            person_type=person_type,
            student=student,
            staff=staff,
            person_name=(request.POST.get('person_name') or '').strip(),
            phone=(request.POST.get('phone') or '').strip(),
            organization=(request.POST.get('organization') or '').strip(),
            destination=(request.POST.get('destination') or '').strip(),
            reason=(request.POST.get('reason') or '').strip(),
            luggage_detail=(request.POST.get('luggage_detail') or '').strip(),
            expected_return_time=_datetime_or_none(request.POST.get('expected_return_time')),
            issued_by=request.user,
        )
        messages.success(request, 'Gate pass created successfully.')
        return redirect('gatepass_print', gatepass_id=record.id)
    return render(request, 'gatepass_form.html', {'students': students, 'staff_members': staff_members})


@staff_required
def gatepass_print(request, gatepass_id):
    record = get_object_or_404(GatePass.objects.select_related('student', 'staff', 'issued_by'), id=gatepass_id)
    return render(request, 'out_slip.html', {'record': record, 'print_date': timezone.localdate()})


@staff_required
def mark_gatepass_returned(request, gatepass_id):
    record = get_object_or_404(GatePass, id=gatepass_id)
    record.status = GatePass.STATUS_RETURNED
    record.returned_at = timezone.now()
    record.save(update_fields=['status', 'returned_at'])
    messages.success(request, 'Gate pass marked returned.')
    return redirect('gatepass_dashboard')
