from django.conf import settings
from django.db import models

from .models import Role, Staff


class SchoolBrandProfile(models.Model):
    school_name = models.CharField(max_length=180, default="Government Middle School Shalgah")
    campus_code = models.CharField(max_length=80, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=80, blank=True)
    email = models.EmailField(blank=True)
    main_logo_path = models.CharField(max_length=255, blank=True)
    watermark_logo_path = models.CharField(max_length=255, blank=True)
    primary_color = models.CharField(max_length=20, default="#2b002d")
    secondary_color = models.CharField(max_length=20, default="#6f1b78")
    accent_color = models.CharField(max_length=20, default="#ffe266")
    is_active = models.BooleanField(default=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_school_brand_profiles",
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "school"
        ordering = ["-is_active", "school_name"]
        indexes = [models.Index(fields=["is_active"], name="school_brand_active_idx")]

    def __str__(self):
        return self.school_name


class UserProfileSetting(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="school_profile_setting")
    display_name = models.CharField(max_length=150, blank=True)
    profile_photo_path = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=80, blank=True)
    note = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "school"
        ordering = ["user__username"]

    def __str__(self):
        return self.display_name or self.user.get_username()


class StaffLoginProfile(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name="login_profile")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_login_profile")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_staff_login_profiles",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "school"
        ordering = ["staff__name"]

    def __str__(self):
        return f"Staff login: {self.staff.name} -> {self.user.username}"


class RoleProfileRule(models.Model):
    role = models.OneToOneField(Role, on_delete=models.CASCADE, related_name="profile_rule")
    can_manage_branding = models.BooleanField(default=False)
    can_upload_self_photo = models.BooleanField(default=True)
    can_create_staff_accounts = models.BooleanField(default=False)
    can_change_own_password = models.BooleanField(default=True)
    can_manage_role_rules = models.BooleanField(default=False)
    dashboard_scope = models.CharField(max_length=120, default="standard")
    note = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["role__name"]

    def __str__(self):
        return f"Rules: {self.role.name}"
