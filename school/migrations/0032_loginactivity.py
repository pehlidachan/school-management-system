# Generated manually for Phase 2.0 login activity audit

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("school", "0031_seed_staff_roles"),
    ]

    operations = [
        migrations.CreateModel(
            name="LoginActivity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("username_entered", models.CharField(blank=True, max_length=150)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("forwarded_for", models.TextField(blank=True)),
                ("user_agent", models.TextField(blank=True)),
                ("path", models.CharField(blank=True, max_length=255)),
                ("method", models.CharField(blank=True, max_length=10)),
                ("is_successful", models.BooleanField(default=False)),
                ("failure_reason", models.CharField(blank=True, max_length=255)),
                ("session_key", models.CharField(blank=True, max_length=100)),
                ("role_snapshot", models.CharField(blank=True, max_length=255)),
                ("city", models.CharField(blank=True, max_length=120)),
                ("region", models.CharField(blank=True, max_length=120)),
                ("country_code", models.CharField(blank=True, max_length=10)),
                ("country_name", models.CharField(blank=True, max_length=120)),
                ("latitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ("longitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ("timezone", models.CharField(blank=True, max_length=80)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="login_activities",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="loginactivity",
            index=models.Index(fields=["created_at"], name="school_logi_created_5c920b_idx"),
        ),
        migrations.AddIndex(
            model_name="loginactivity",
            index=models.Index(fields=["ip_address"], name="school_logi_ip_addr_54731c_idx"),
        ),
        migrations.AddIndex(
            model_name="loginactivity",
            index=models.Index(fields=["is_successful"], name="school_logi_is_succ_276d20_idx"),
        ),
        migrations.AddIndex(
            model_name="loginactivity",
            index=models.Index(fields=["username_entered"], name="school_logi_usernam_fa16f4_idx"),
        ),
    ]
