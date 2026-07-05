from django.shortcuts import render
from .access_control import admin_required


def _chart_uri(kind, labels, values, title):
    try:
        import base64
        import io
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import pandas as pd

        df = pd.DataFrame({'label': labels, 'value': values})
        fig, ax = plt.subplots(figsize=(4.6, 2.6))
        if kind == 'line':
            ax.plot(df['label'], df['value'], marker='o', linewidth=2)
        elif kind == 'bar':
            ax.bar(df['label'], df['value'])
        elif kind == 'pie':
            ax.pie(df['value'], labels=df['label'], autopct='%1.0f%%', startangle=90)
            ax.axis('equal')
        ax.set_title(title, fontsize=11, fontweight='bold')
        if kind != 'pie':
            ax.grid(True, alpha=0.25)
            ax.tick_params(axis='x', labelrotation=15)
        fig.tight_layout()
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=130, bbox_inches='tight', transparent=True)
        plt.close(fig)
        return 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode('ascii')
    except Exception:
        return ''


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

    data['line_chart'] = _chart_uri(
        'line',
        ['Students', 'Staff', 'Classes', 'Subjects'],
        [data['total_students'], data['total_staff'], data['total_classes'], data['total_subjects']],
        'Core Records Overview',
    )
    data['bar_chart'] = _chart_uri(
        'bar',
        ['Complaints', 'Admissions', 'Jobs'],
        [data['total_parent_complaints'], data['total_online_admissions'], data['total_job_applications']],
        'Online Requests',
    )
    data['pie_chart'] = _chart_uri(
        'pie',
        ['Student IDs', 'Parent IDs', 'Staff'],
        [data['total_student_logins'], data['total_parent_logins'], data['total_staff']],
        'Portal Account Mix',
    )
    data['analytics_total'] = data['total_parent_complaints'] + data['total_online_admissions'] + data['total_job_applications']
    return render(request, 'admin_portal_online.html', data)
