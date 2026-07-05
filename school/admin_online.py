from django.shortcuts import render
from .access_control import admin_required


@admin_required
def portal(request):
    from . import models
    from . import public_models
    data = {
        'total_students': models.Student.objects.count(),
        'total_staff': models.Staff.objects.count(),
        'total_grades': models.Grade.objects.count(),
        'total_subjects': models.Subject.objects.count(),
        'total_classes': models.ClassAndTiming.objects.count(),
        'total_class_incharges': models.ClassIncharge.objects.count(),
        'total_roles': models.Role.objects.count(),
        'total_genders': models.Gender.objects.count(),
        'total_guardian_relations': models.GuardianRelation.objects.count(),
        'total_employment_statuses': models.EmploymentStatus.objects.count(),
        'total_student_logins': models.StudentUserProfile.objects.count(),
        'total_parent_logins': models.ParentProfile.objects.count(),
        'total_parent_complaints': public_models.ParentComplaint.objects.count(),
        'total_online_admissions': public_models.OnlineAdmissionApplication.objects.count(),
        'total_job_applications': public_models.JobApplication.objects.count(),
    }
    return render(request, 'admin_portal_online.html', data)
