# Generated manually for Phase 2.1 Attendance MVP

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("school", "0033_merge_loginactivity_student_parent_profiles"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttendanceSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("attendance_date", models.DateField()),
                ("note", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("grade", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attendance_sessions", to="school.grade")),
                ("taken_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="taken_attendance_sessions", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-attendance_date", "grade__name"]},
        ),
        migrations.CreateModel(
            name="StudentAttendance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("present", "Present"), ("absent", "Absent"), ("late", "Late"), ("leave", "Leave")], default="present", max_length=20)),
                ("remarks", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("marked_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="marked_student_attendance", to=settings.AUTH_USER_MODEL)),
                ("session", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="records", to="school.attendancesession")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attendance_records", to="school.student")),
            ],
            options={"ordering": ["student__name"]},
        ),
        migrations.AddConstraint(
            model_name="attendancesession",
            constraint=models.UniqueConstraint(fields=("grade", "attendance_date"), name="unique_grade_attendance_date"),
        ),
        migrations.AddIndex(
            model_name="attendancesession",
            index=models.Index(fields=["attendance_date"], name="school_atte_attenda_8eaa5f_idx"),
        ),
        migrations.AddIndex(
            model_name="attendancesession",
            index=models.Index(fields=["grade", "attendance_date"], name="school_atte_grade_i_226646_idx"),
        ),
        migrations.AddConstraint(
            model_name="studentattendance",
            constraint=models.UniqueConstraint(fields=("session", "student"), name="unique_student_attendance_per_session"),
        ),
        migrations.AddIndex(
            model_name="studentattendance",
            index=models.Index(fields=["status"], name="school_stud_status_3f8049_idx"),
        ),
        migrations.AddIndex(
            model_name="studentattendance",
            index=models.Index(fields=["student", "status"], name="school_stud_student_3a9ed6_idx"),
        ),
    ]
