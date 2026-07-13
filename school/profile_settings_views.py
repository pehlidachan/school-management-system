import base64
import re

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .access_control import admin_required
from .media_utils import save_person_file
from .models import Role, Staff
from .profile_settings_models import (
    RoleProfileRule,
    SchoolBrandProfile,
    StaffLoginProfile,
    UserProfileSetting,
)


HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


def _safe_color(value, fallback):
    value = (value or "").strip()
    return value if HEX_COLOR_RE.match(value) else fallback


def _camera_upload(data_url, name="camera.jpg"):
    if not data_url or ";base64," not in data_url:
        return None
    header, encoded = data_url.split(";base64,", 1)
    ext = ".jpg"
    content_type = "image/jpeg"
    if "image/png" in header:
        ext = ".png"
        content_type = "image/png"
    elif "image/webp" in header:
        ext = ".webp"
        content_type = "image/webp"
    try:
        payload = base64.b64decode(encoded)
    except Exception:
        return None
    return SimpleUploadedFile(name.replace(".jpg", ext), payload, content_type=content_type)


def _get_brand():
    brand = SchoolBrandProfile.objects.filter(is_active=True).first()
    if not brand:
        brand = SchoolBrandProfile.objects.create(is_active=True)
    return brand


def _sync_role_rules():
    for role in Role.objects.all():
        rule, created = RoleProfileRule.objects.get_or_create(role=role)
        if created and role.name in {"School Admin", "Principal"}:
            rule.can_manage_branding = True
            rule.can_create_staff_accounts = True
            rule.can_manage_role_rules = True
            rule.dashboard_scope = "full-admin"
            rule.save()


def _save_optional_upload(area, record_id, uploaded_file):
    if not uploaded_file:
        return ""
    saved_path = save_person_file(area, record_id, uploaded_file)
    return saved_path or ""


@admin_required
def admin_profile_center(request):
    brand = _get_brand()
    profile, _ = UserProfileSetting.objects.get_or_create(user=request.user)
    _sync_role_rules()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "save_brand":
            brand.school_name = (request.POST.get("school_name") or brand.school_name).strip()
            brand.campus_code = (request.POST.get("campus_code") or "").strip()
            brand.address = (request.POST.get("address") or "").strip()
            brand.phone = (request.POST.get("phone") or "").strip()
            brand.email = (request.POST.get("email") or "").strip()
            brand.primary_color = _safe_color(request.POST.get("primary_color"), brand.primary_color)
            brand.secondary_color = _safe_color(request.POST.get("secondary_color"), brand.secondary_color)
            brand.accent_color = _safe_color(request.POST.get("accent_color"), brand.accent_color)
            brand.updated_by = request.user
            brand.save()

            uploaded_labels = []
            main_logo = request.FILES.get("main_logo")
            watermark_logo = request.FILES.get("watermark_logo")
            main_logo_path = _save_optional_upload("school_brand_main_logo", brand.id, main_logo)
            watermark_logo_path = _save_optional_upload("school_brand_watermark_logo", brand.id, watermark_logo)
            if main_logo_path:
                brand.main_logo_path = main_logo_path
                uploaded_labels.append("main logo")
            if watermark_logo_path:
                brand.watermark_logo_path = watermark_logo_path
                uploaded_labels.append("watermark logo")
            if uploaded_labels:
                brand.updated_by = request.user
                brand.save(update_fields=["main_logo_path", "watermark_logo_path", "updated_by", "updated_at"])
                messages.success(request, f"School branding saved with uploaded {', '.join(uploaded_labels)}.")
            else:
                messages.success(request, "School branding text/colors saved. No new logo file was selected.")
            return redirect("admin_profile_center")

        if action == "save_profile":
            profile.display_name = (request.POST.get("display_name") or "").strip()
            profile.phone = (request.POST.get("phone") or "").strip()
            profile.note = (request.POST.get("note") or "").strip()
            profile.save()

            if request.POST.get("remove_profile_photo"):
                profile.profile_photo_path = ""
                profile.save(update_fields=["profile_photo_path", "updated_at"])
                messages.success(request, "Profile details saved and profile photo removed.")
                return redirect("admin_profile_center")

            upload = request.FILES.get("profile_photo") or _camera_upload(request.POST.get("camera_image_data"), "profile_camera.jpg")
            uploaded_path = _save_optional_upload("user_profile_photos", request.user.id, upload)
            if uploaded_path:
                profile.profile_photo_path = uploaded_path
                profile.save(update_fields=["profile_photo_path", "updated_at"])
                messages.success(request, "Profile saved and new profile picture uploaded successfully.")
            else:
                messages.success(request, "Profile details saved. No new picture file was selected.")
            return redirect("admin_profile_center")

        if action == "change_password":
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully.")
                return redirect("admin_profile_center")
            messages.error(request, "Password change failed. Please check the password rules.")

        if action == "create_staff_account":
            staff = get_object_or_404(Staff, id=request.POST.get("staff_id"))
            username = (request.POST.get("username") or "").strip()
            password = request.POST.get("password") or ""
            group_name = (request.POST.get("group_name") or "Teacher").strip()
            if not username or not password:
                messages.error(request, "Username and password are required for staff account.")
                return redirect("admin_profile_center")
            if StaffLoginProfile.objects.filter(staff=staff).exists():
                messages.warning(request, "This staff member already has a login account.")
                return redirect("admin_profile_center")
            if User.objects.filter(username__iexact=username).exists():
                messages.error(request, "This username already exists.")
                return redirect("admin_profile_center")
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=staff.email or "",
                    first_name=staff.name,
                    is_staff=bool(request.POST.get("is_staff")),
                )
                group, _ = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)
                StaffLoginProfile.objects.create(staff=staff, user=user, created_by=request.user)
            messages.success(request, f"Staff login created for {staff.name}.")
            return redirect("admin_profile_center")

        if action == "save_role_rule":
            rule = get_object_or_404(RoleProfileRule, id=request.POST.get("rule_id"))
            rule.can_manage_branding = bool(request.POST.get("can_manage_branding"))
            rule.can_upload_self_photo = bool(request.POST.get("can_upload_self_photo"))
            rule.can_create_staff_accounts = bool(request.POST.get("can_create_staff_accounts"))
            rule.can_change_own_password = bool(request.POST.get("can_change_own_password"))
            rule.can_manage_role_rules = bool(request.POST.get("can_manage_role_rules"))
            rule.dashboard_scope = (request.POST.get("dashboard_scope") or "standard").strip()
            rule.note = (request.POST.get("note") or "").strip()
            rule.save()
            messages.success(request, f"Role rule updated for {rule.role.name}.")
            return redirect("admin_profile_center")

    password_form = PasswordChangeForm(request.user)
    staff_without_login = Staff.objects.filter(status=True).exclude(login_profile__isnull=False).order_by("name")[:200]
    role_rules = RoleProfileRule.objects.select_related("role").all()
    staff_accounts = StaffLoginProfile.objects.select_related("staff", "user", "created_by")[:100]
    groups = Group.objects.order_by("name")

    return render(request, "admin_profile_center.html", {
        "brand": brand,
        "profile": profile,
        "password_form": password_form,
        "staff_without_login": staff_without_login,
        "staff_accounts": staff_accounts,
        "role_rules": role_rules,
        "groups": groups,
    })
