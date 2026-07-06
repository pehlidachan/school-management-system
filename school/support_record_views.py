from datetime import datetime

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .access_control import admin_required
from .media_utils import save_person_file
from .models import EmploymentStatus, Gender
from .non_teaching_models import NonTeachingStaff


def _date_or_none(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


def _upload(request):
    return request.FILES.get('person_image') or request.FILES.get('photo_capture') or request.FILES.get('image')


def _save(request, record=None):
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
    save_person_file('support', record.id, _upload(request))
    return record


@admin_required
def add_record(request):
    if request.method == 'POST':
        record = _save(request)
        messages.success(request, 'Non-teaching staff record added.')
        return redirect('non_teaching_staff_detail', record_id=record.id)
    return render(request, 'non_teaching_staff_form.html', {'genders': Gender.objects.all(), 'employment_statuses': EmploymentStatus.objects.all(), 'record': None})


@admin_required
def edit_record(request, record_id):
    record = get_object_or_404(NonTeachingStaff, id=record_id)
    if request.method == 'POST':
        _save(request, record)
        messages.success(request, 'Non-teaching staff record updated.')
        return redirect('non_teaching_staff_detail', record_id=record.id)
    return render(request, 'non_teaching_staff_form.html', {'genders': Gender.objects.all(), 'employment_statuses': EmploymentStatus.objects.all(), 'record': record})
