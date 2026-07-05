# Phase 3.0 Results MVP migration

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("school", "0039_messaging_mvp"),
    ]

    operations = [
        migrations.CreateModel(
            name="Exam",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=180)),
                ("start_date", models.DateField(default=django.utils.timezone.localdate)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("is_published", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_exams", to=settings.AUTH_USER_MODEL)),
                ("grade", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="exams", to="school.grade")),
            ],
            options={"ordering": ["-start_date", "grade__name", "name"]},
        ),
        migrations.CreateModel(
            name="ExamSubject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("total_marks", models.DecimalField(decimal_places=2, default=100, max_digits=7)),
                ("passing_marks", models.DecimalField(decimal_places=2, default=33, max_digits=7)),
                ("exam", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="exam_subjects", to="school.exam")),
                ("subject", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="exam_subjects", to="school.subject")),
            ],
            options={"ordering": ["subject__name"]},
        ),
        migrations.CreateModel(
            name="StudentMark",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("marks_obtained", models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ("remarks", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("exam_subject", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="marks", to="school.examsubject")),
                ("marked_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="marked_exam_results", to=settings.AUTH_USER_MODEL)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="exam_marks", to="school.student")),
            ],
            options={"ordering": ["student__name"]},
        ),
        migrations.AddConstraint(model_name="examsubject", constraint=models.UniqueConstraint(fields=("exam", "subject"), name="unique_subject_per_exam")),
        migrations.AddConstraint(model_name="studentmark", constraint=models.UniqueConstraint(fields=("exam_subject", "student"), name="unique_student_mark_per_exam_subject")),
    ]
