from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .login_audit import record_login_activity


def user_login(request):
    """Audited login view.

    This overrides the older login route at project URL level and records both
    successful and failed login attempts for future Streamlit analytics.
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'login.html')

    if request.user.is_authenticated:
        record_login_activity(
            request,
            username_entered=request.user.username,
            user=request.user,
            is_successful=True,
            failure_reason='already_authenticated',
        )
        messages.warning(request, 'You have already logged in!')
        return redirect('dashboard')

    username = (request.POST.get('username') or '').strip()
    password = request.POST.get('password') or ''

    if not username or not password:
        record_login_activity(
            request,
            username_entered=username,
            is_successful=False,
            failure_reason='missing_username_or_password',
        )
        messages.error(request, 'Please enter both username and password!')
        return redirect('login')

    user = authenticate(request, username=username, password=password)
    if user is None:
        record_login_activity(
            request,
            username_entered=username,
            is_successful=False,
            failure_reason='invalid_credentials_or_inactive',
        )
        messages.error(request, 'Invalid credentials, or your account is waiting for admin approval.')
        return redirect('login')

    login(request, user)
    record_login_activity(
        request,
        username_entered=username,
        user=user,
        is_successful=True,
    )
    messages.success(request, 'User logged in successfully!')
    return redirect('dashboard')
