from __future__ import annotations

from typing import Optional

from django.contrib.auth.models import AnonymousUser

from .models import LoginActivity


PRIVATE_OR_LOCAL_IPS = {"127.0.0.1", "::1", "localhost"}


def get_client_ip(request) -> tuple[Optional[str], str]:
    """Return best-effort client IP and full forwarded-for chain.

    In local development this is usually 127.0.0.1 or ::1. In production,
    correct real IP depends on reverse proxy headers. We save both the chosen
    IP and the full X-Forwarded-For chain for later auditing.
    """
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        first_ip = forwarded_for.split(",")[0].strip()
        return first_ip or None, forwarded_for

    real_ip = request.META.get("HTTP_X_REAL_IP", "")
    if real_ip:
        return real_ip.strip() or None, ""

    remote_addr = request.META.get("REMOTE_ADDR", "")
    return remote_addr.strip() or None, ""


def get_role_snapshot(user) -> str:
    if not user or isinstance(user, AnonymousUser) or not user.is_authenticated:
        return ""

    roles = []
    if user.is_superuser:
        roles.append("Superuser")
    if user.is_staff:
        roles.append("Django Staff")

    group_names = list(user.groups.values_list("name", flat=True))
    roles.extend(group_names)

    if hasattr(user, "student_profile"):
        roles.append("StudentProfile")
    if hasattr(user, "parent_profile"):
        roles.append("ParentProfile")

    return ", ".join(dict.fromkeys(roles))[:255]


def record_login_activity(
    request,
    *,
    username_entered: str = "",
    user=None,
    is_successful: bool = False,
    failure_reason: str = "",
) -> None:
    """Write one login audit row without breaking the login flow.

    Audit logging must never block a user from logging in, so errors are
    swallowed intentionally. During development, inspect Django Admin or DB.
    """
    try:
        ip_address, forwarded_for = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        session_key = getattr(request.session, "session_key", "") or ""

        LoginActivity.objects.create(
            user=user if getattr(user, "is_authenticated", False) else None,
            username_entered=(username_entered or "")[:150],
            ip_address=ip_address,
            forwarded_for=forwarded_for,
            user_agent=user_agent,
            path=request.path[:255],
            method=request.method[:10],
            is_successful=is_successful,
            failure_reason=(failure_reason or "")[:255],
            session_key=session_key[:100],
            role_snapshot=get_role_snapshot(user),
        )
    except Exception:
        # Keep authentication flow safe even if audit table is not migrated yet.
        pass
