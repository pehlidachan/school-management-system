from django.shortcuts import render

from .access_control import admin_required
from .public_models import JobApplication, OnlineAdmissionApplication, ParentComplaint


@admin_required
def online_requests_center(request):
    return render(request, 'online_requests_center.html', {
        'complaint_total': ParentComplaint.objects.count(),
        'admission_total': OnlineAdmissionApplication.objects.count(),
        'job_total': JobApplication.objects.count(),
        'complaint_new': ParentComplaint.objects.filter(status='new').count(),
        'admission_new': OnlineAdmissionApplication.objects.filter(status='new').count(),
        'job_new': JobApplication.objects.filter(status='new').count(),
        'recent_complaints': ParentComplaint.objects.all()[:5],
        'recent_admissions': OnlineAdmissionApplication.objects.all()[:5],
        'recent_jobs': JobApplication.objects.all()[:5],
    })
