from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .access_control import (
    is_account_creator,
    is_school_admin,
    is_school_parent,
    is_school_student,
    is_teacher_like,
)


@login_required(login_url='login')
def dashboard(request):
    """Role-aware landing page.

    This keeps /dashboard/ visible for every signed-in user and shows clear
    action cards instead of silently redirecting back to Home.
    """
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
    return render(request, 'dashboard.html', context)
