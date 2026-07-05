"""Access-control helpers for the school app.

This module keeps role checks in one place instead of repeating
``request.user.is_authenticated`` and ``request.user.is_superuser`` in every view.
"""
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

SCHOOL_ADMIN = "School Admin"
PRINCIPAL = "Principal"
HEAD_OF_DEPARTMENT = "Head of Department"
TEACHER = "Teacher"
STUDENT = "Student"
PARENT = "Parent"
ACCOUNTANT = "Accountant"

ADMIN_GROUPS = {SCHOOL_ADMIN, PRINCIPAL}
STAFF_GROUPS = {SCHOOL_ADMIN, PRINCIPAL, HEAD_OF_DEPARTMENT, TEACHER, ACCOUNTANT}
STUDENT_GROUPS = {STUDENT}
PARENT_GROUPS = {PARENT}
ACCOUNT_CREATOR_GROUPS = {SCHOOL_ADMIN, PRINCIPAL, ACCOUNTANT}
FINANCE_GROUPS = {SCHOOL_ADMIN, PRINCIPAL, ACCOUNTANT}


def user_in_any_group(user, group_names):
    """Return True when the user belongs to any of the named Django groups."""
    if not user.is_authenticated:
        return False
    return user.groups.filter(name__in=group_names).exists()


def is_school_admin(user):
    """Admins are Django superusers or users in the School Admin/Principal groups."""
    return bool(
        user.is_authenticated
        and (user.is_superuser or user_in_any_group(user, ADMIN_GROUPS))
    )


def is_account_creator(user):
    """Users allowed to create/reset student and parent login IDs."""
    return bool(
        user.is_authenticated
        and (user.is_superuser or user_in_any_group(user, ACCOUNT_CREATOR_GROUPS))
    )


def is_finance_user(user):
    """Finance users include School Admin, Principal and Accountant."""
    return bool(
        user.is_authenticated
        and (user.is_superuser or user_in_any_group(user, FINANCE_GROUPS))
    )


def is_school_staff(user):
    """Staff-side users include admins, principals, HODs, teachers and accountants."""
    return bool(
        user.is_authenticated
        and (user.is_superuser or user.is_staff or user_in_any_group(user, STAFF_GROUPS))
    )


def is_teacher_like(user):
    """Teaching-side dashboard users: teacher or head of department."""
    return bool(
        user.is_authenticated
        and user_in_any_group(user, {TEACHER, HEAD_OF_DEPARTMENT})
    )


def is_school_student(user):
    """Student users must belong to the Student group."""
    return bool(user.is_authenticated and user_in_any_group(user, STUDENT_GROUPS))


def is_school_parent(user):
    """Parent users must belong to the Parent group."""
    return bool(user.is_authenticated and user_in_any_group(user, PARENT_GROUPS))


def _guard(view_func, allowed_check, denial_message):
    @login_required(login_url="login")
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if allowed_check(request.user):
            return view_func(request, *args, **kwargs)
        messages.warning(request, denial_message)
        return redirect("home")

    return _wrapped_view


def admin_required(view_func):
    """Require Django superuser, School Admin group, or Principal group."""
    return _guard(view_func, is_school_admin, "This page is for authorized school admins only.")


def account_creator_required(view_func):
    """Require School Admin, Principal, Accountant, or superuser."""
    return _guard(view_func, is_account_creator, "Only Principal, Accountant, or School Admin can create login IDs.")


def finance_required(view_func):
    """Require School Admin, Principal, Accountant, or superuser."""
    return _guard(view_func, is_finance_user, "Only Principal, Accountant, or School Admin can access finance.")


def staff_required(view_func):
    """Require a staff-side user."""
    return _guard(view_func, is_school_staff, "This page is for school staff only.")


def student_required(view_func):
    """Require a student-side user."""
    return _guard(view_func, is_school_student, "This page is for students only.")


def parent_required(view_func):
    """Require a parent-side user."""
    return _guard(view_func, is_school_parent, "This page is for parents only.")
