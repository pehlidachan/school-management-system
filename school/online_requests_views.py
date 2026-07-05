from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .access_control import admin_required
from .public_models import JobApplication, OnlineAdmissionApplication, ParentComplaint


def _filter_status(queryset, status):
    if status:
        return queryset.filter(status=status)
    return queryset


@admin_required
def parent_complaints(request):
    status = request.GET.get('status') or ''
    records = _filter_status(ParentComplaint.objects.all(), status)[:300]
    return render(request, 'online_parent_complaints.html', {
        'records': records,
        'selected_status': status,
        'total_records': ParentComplaint.objects.count(),
    })


@admin_required
def online_admissions(request):
    status = request.GET.get('status') or ''
    records = _filter_status(OnlineAdmissionApplication.objects.all(), status)[:300]
    return render(request, 'online_admissions_admin.html', {
        'records': records,
        'selected_status': status,
        'total_records': OnlineAdmissionApplication.objects.count(),
    })


@admin_required
def job_applications(request):
    status = request.GET.get('status') or ''
    records = _filter_status(JobApplication.objects.all(), status)[:300]
    return render(request, 'online_job_applications.html', {
        'records': records,
        'selected_status': status,
        'total_records': JobApplication.objects.count(),
    })


@admin_required
def update_parent_complaint_status(request, record_id):
    if request.method == 'POST':
        record = get_object_or_404(ParentComplaint, id=record_id)
        record.status = request.POST.get('status') or record.status
        record.save(update_fields=['status'])
        messages.success(request, 'Complaint status updated.')
    return redirect('online_parent_complaints')


@admin_required
def update_admission_status(request, record_id):
    if request.method == 'POST':
        record = get_object_or_404(OnlineAdmissionApplication, id=record_id)
        record.status = request.POST.get('status') or record.status
        record.save(update_fields=['status'])
        messages.success(request, 'Admission status updated.')
    return redirect('online_admissions_admin')


@admin_required
def update_job_status(request, record_id):
    if request.method == 'POST':
        record = get_object_or_404(JobApplication, id=record_id)
        record.status = request.POST.get('status') or record.status
        record.save(update_fields=['status'])
        messages.success(request, 'Job application status updated.')
    return redirect('online_job_applications')
