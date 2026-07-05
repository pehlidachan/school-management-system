from django.shortcuts import render

from .access_control import admin_required


@admin_required
def records(request):
    from . import public_models
    qs = public_models.JobApplication.objects.all()[:300]
    return render(request, 'work_list.html', {
        'records': qs,
        'total_records': public_models.JobApplication.objects.count(),
    })
