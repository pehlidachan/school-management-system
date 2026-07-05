# Generated manually for Phase 2.6 Notice Board MVP

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("school", "0035_finance_mvp"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("body", models.TextField()),
                ("audience", models.CharField(choices=[("all", "All"), ("students", "Students"), ("parents", "Parents"), ("teachers", "Teachers"), ("staff", "Staff")], default="all", max_length=20)),
                ("priority", models.CharField(choices=[("normal", "Normal"), ("important", "Important"), ("urgent", "Urgent")], default="normal", max_length=20)),
                ("publish_date", models.DateField(default=django.utils.timezone.localdate)),
                ("expiry_date", models.DateField(blank=True, null=True)),
                ("is_published", models.BooleanField(default=True)),
                ("view_count", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_notices", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-publish_date", "-created_at"]},
        ),
        migrations.AddIndex(model_name="notice", index=models.Index(fields=["publish_date"], name="school_noti_publish_9ba5e2_idx")),
        migrations.AddIndex(model_name="notice", index=models.Index(fields=["audience"], name="school_noti_audienc_20c79a_idx")),
        migrations.AddIndex(model_name="notice", index=models.Index(fields=["priority"], name="school_noti_priorit_84cd7c_idx")),
        migrations.AddIndex(model_name="notice", index=models.Index(fields=["is_published"], name="school_noti_is_publ_1f75b9_idx")),
    ]
