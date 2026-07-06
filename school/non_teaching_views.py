from datetime import datetime

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .access_control import admin_required
from .models import EmploymentStatus, Gender
from .non_teaching_models import NonTeachingStaff


def _date_or_none(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


def _save_record(request, record=None):
    if record is None:
        record = NonTeachingStaff()
    record.name = (request.POST.get('name') or '').strip()
    record.age = int(request.POST.get('age') or 0) or None
    record.dob = _date_or_none(request.POST.get('dob'))
    record.gender_id = request.POST.get('gender') or None
    record.appointment = (request.POST.get('appointment') or '').strip()
    record.work_detail = (request.POST.get('work_detail') or '').strip()
    record.department = (request.POST.get('department') or '').strip()
    record.qualification = (request.POST.get('qualification') or '').strip()
    record.experience = (request.POST.get('experience') or '').strip()
    record.email = (request.POST.get('email') or '').strip()
    record.phone = (request.POST.get('phone') or '').strip()
    record.emergency_phone = (request.POST.get('emergency_phone') or '').strip()
    record.address = (request.POST.get('address') or '').strip()
    record.joining_date = _date_or_none(request.POST.get('joining_date'))
    record.salary = (request.POST.get('salary') or '').strip()
    record.employment_status_id = request.POST.get('employment_status') or None
    record.contract_details = (request.POST.get('contract_details') or '').strip()
    record.status = bool(request.POST.get('status'))
    record.save()
    return record


@admin_required
def non_teaching_staff_list(request):
    query = (request.GET.get('q') or '').strip()
    status = request.GET.get('status') or ''
    records = NonTeachingStaff.objects.select_related('gender', 'employment_status').order_by('name')
    if query:
        records = records.filter(Q(name__icontains=query) | Q(appointment__icontains=query) | Q(work_detail__icontains=query) | Q(phone__icontains=query))
    if status == 'active':
        records = records.filter(status=True)
    elif status == 'inactive':
        records = records.filter(status=False)
    return render(request, 'non_teaching_staff_list.html', {'records': records[:300], 'q': query, 'selected_status': status})


@admin_required
def add_non_teaching_staff(request):
    if request.method == 'POST':
        record = _save_record(request)
        messages.success(request, 'Non-teaching staff record added.')
        return redirect('non_teaching_staff_detail', record_id=record.id)
    return render(request, 'non_teaching_staff_form.html', {'genders': Gender.objects.all(), 'employment_statuses': EmploymentStatus.objects.all(), 'record': None})


@admin_required
def edit_non_teaching_staff(request, record_id):
    record = get_object_or_404(NonTeachingStaff, id=record_id)
    if request.method == 'POST':
        _save_record(request, record)
        messages.success(request, 'Non-teaching staff record updated.')
        return redirect('non_teaching_staff_detail', record_id=record.id)
    return render(request, 'non_teaching_staff_form.html', {'genders': Gender.objects.all(), 'employment_statuses': EmploymentStatus.objects.all(), 'record': record})


@admin_required
def non_teaching_staff_detail(request, record_id):
    record = get_object_or_404(NonTeachingStaff.objects.select_related('gender', 'employment_status'), id=record_id)
    return render(request, 'non_teaching_staff_detail.html', {'record': record})


@admin_required
def change_non_teaching_staff_status(request, record_id):
    record = get_object_or_404(NonTeachingStaff, id=record_id)
    record.status = not record.status
    record.save(update_fields=['status'])
    messages.success(request, 'Status changed.')
    return redirect('non_teaching_staff_list')
