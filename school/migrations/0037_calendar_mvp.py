# Generated manually for Phase 2.7 Calendar MVP

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("school", "0036_notice_board_mvp"),
    ]

    operations = [
        migrations.CreateModel(
            name="SchoolCalendarEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("event_type", models.CharField(choices=[("event", "Event"), ("holiday", "Holiday"), ("exam", "Exam"), ("meeting", "Meeting"), ("deadline", "Deadline")], default="event", max_length=20)),
                ("audience", models.CharField(choices=[("all", "All"), ("students", "Students"), ("parents", "Parents"), ("teachers", "Teachers"), ("staff", "Staff")], default="all", max_length=20)),
                ("event_date", models.DateField(default=django.utils.timezone.localdate)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("start_time", models.TimeField(blank=True, null=True)),
                ("end_time", models.TimeField(blank=True, null=True)),
                ("location", models.CharField(blank=True, max_length=220)),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_calendar_events", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["event_date", "start_time", "title"]},
        ),
        migrations.AddIndex(model_name="schoolcalendarevent", index=models.Index(fields=["event_date"], name="school_scho_event_d_9ebfd7_idx")),
        migrations.AddIndex(model_name="schoolcalendarevent", index=models.Index(fields=["event_type"], name="school_scho_event_t_2f0bc3_idx")),
        migrations.AddIndex(model_name="schoolcalendarevent", index=models.Index(fields=["audience"], name="school_scho_audienc_119ef4_idx")),
        migrations.AddIndex(model_name="schoolcalendarevent", index=models.Index(fields=["is_active"], name="school_scho_is_acti_4e5fd2_idx")),
    ]
