from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .access_control import (
    is_account_creator,
    is_school_admin,
    is_school_parent,
    is_school_student,
    is_teacher_like,
)


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


@login_required(login_url='login')
def dashboard(request):
    """Role-aware landing page."""
    user = request.user
    is_admin_user = is_school_admin(user)
    is_account_creator_user = is_account_creator(user)
    is_parent_user = is_school_parent(user)
    is_student_user = is_school_student(user)
    is_teacher_user = is_teacher_like(user)

    context = {
        'is_admin_user': is_admin_user,
        'is_account_creator_user': is_account_creator_user,
        'is_parent_user': is_parent_user,
        'is_student_user': is_student_user,
        'is_teacher_user': is_teacher_user,
        'has_any_school_area': any([
            is_admin_user,
            is_account_creator_user,
            is_parent_user,
            is_student_user,
            is_teacher_user,
        ]),
    }

    from . import models
    try:
        from . import public_models
        complaints = public_models.ParentComplaint.objects.count()
        admissions = public_models.OnlineAdmissionApplication.objects.count()
        jobs = public_models.JobApplication.objects.count()
    except Exception:
        complaints = admissions = jobs = 0

    students = models.Student.objects.count()
    staff = models.Staff.objects.count()
    classes = models.ClassAndTiming.objects.count()
    subjects = models.Subject.objects.count()
    student_ids = models.StudentUserProfile.objects.count()
    parent_ids = models.ParentProfile.objects.count()

    context.update({
        'show_dashboard_analytics': True,
        'dash_total_students': students,
        'dash_total_staff': staff,
        'dash_total_classes': classes,
        'dash_total_subjects': subjects,
        'dash_total_complaints': complaints,
        'dash_total_admissions': admissions,
        'dash_total_jobs': jobs,
        'dash_analytics_total': complaints + admissions + jobs,
        'dash_line_chart': _chart_uri('line', ['Students', 'Staff', 'Classes', 'Subjects'], [students, staff, classes, subjects], 'Core Records'),
        'dash_bar_chart': _chart_uri('bar', ['Complaints', 'Admissions', 'Jobs'], [complaints, admissions, jobs], 'Online Requests'),
        'dash_pie_chart': _chart_uri('pie', ['Student IDs', 'Parent IDs', 'Staff'], [student_ids, parent_ids, staff], 'Account Mix'),
    })
    return render(request, 'dashboard.html', context)
