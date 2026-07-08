# Generated for admin profile settings MVP on 2026-07-08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0049_vendor_cash_bank_ledger_mvp'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolBrandProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(default='Government Middle School Shalgah', max_length=180)),
                ('campus_code', models.CharField(blank=True, max_length=80)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=80)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('main_logo_path', models.CharField(blank=True, max_length=255)),
                ('watermark_logo_path', models.CharField(blank=True, max_length=255)),
                ('primary_color', models.CharField(default='#2b002d', max_length=20)),
                ('secondary_color', models.CharField(default='#6f1b78', max_length=20)),
                ('accent_color', models.CharField(default='#ffe266', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_school_brand_profiles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-is_active', 'school_name'],
                'indexes': [models.Index(fields=['is_active'], name='school_brand_active_idx')],
            },
        ),
        migrations.CreateModel(
            name='UserProfileSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(blank=True, max_length=150)),
                ('profile_photo_path', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=80)),
                ('note', models.TextField(blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='school_profile_setting', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['user__username']},
        ),
        migrations.CreateModel(
            name='StaffLoginProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_staff_login_profiles', to=settings.AUTH_USER_MODEL)),
                ('staff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='login_profile', to='school.staff')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff_login_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['staff__name']},
        ),
        migrations.CreateModel(
            name='RoleProfileRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_manage_branding', models.BooleanField(default=False)),
                ('can_upload_self_photo', models.BooleanField(default=True)),
                ('can_create_staff_accounts', models.BooleanField(default=False)),
                ('can_change_own_password', models.BooleanField(default=True)),
                ('can_manage_role_rules', models.BooleanField(default=False)),
                ('dashboard_scope', models.CharField(default='standard', max_length=120)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_rule', to='school.role')),
            ],
            options={'ordering': ['role__name']},
        ),
    ]
