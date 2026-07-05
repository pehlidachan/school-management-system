# Generated manually for Phase 2.8 Library MVP

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("school", "0037_calendar_mvp"),
    ]

    operations = [
        migrations.CreateModel(
            name="LibraryBook",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=240)),
                ("author", models.CharField(blank=True, max_length=180)),
                ("isbn", models.CharField(blank=True, max_length=80)),
                ("accession_number", models.CharField(max_length=80, unique=True)),
                ("category", models.CharField(blank=True, max_length=120)),
                ("publisher", models.CharField(blank=True, max_length=180)),
                ("shelf_location", models.CharField(blank=True, max_length=120)),
                ("total_copies", models.PositiveIntegerField(default=1)),
                ("available_copies", models.PositiveIntegerField(default=1)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("added_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="added_library_books", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["title", "author"]},
        ),
        migrations.CreateModel(
            name="LibraryIssue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("issue_date", models.DateField(default=django.utils.timezone.localdate)),
                ("due_date", models.DateField()),
                ("return_date", models.DateField(blank=True, null=True)),
                ("status", models.CharField(choices=[("issued", "Issued"), ("returned", "Returned"), ("overdue", "Overdue")], default="issued", max_length=20)),
                ("remarks", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("book", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="issues", to="school.librarybook")),
                ("issued_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="issued_library_books", to=settings.AUTH_USER_MODEL)),
                ("returned_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="returned_library_books", to=settings.AUTH_USER_MODEL)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="library_issues", to="school.student")),
            ],
            options={"ordering": ["-issue_date", "-created_at"]},
        ),
        migrations.AddIndex(model_name="librarybook", index=models.Index(fields=["title"], name="school_libr_title_70f98d_idx")),
        migrations.AddIndex(model_name="librarybook", index=models.Index(fields=["isbn"], name="school_libr_isbn_31967e_idx")),
        migrations.AddIndex(model_name="librarybook", index=models.Index(fields=["accession_number"], name="school_libr_accessi_9e9df1_idx")),
        migrations.AddIndex(model_name="librarybook", index=models.Index(fields=["category"], name="school_libr_categor_51f62b_idx")),
        migrations.AddIndex(model_name="librarybook", index=models.Index(fields=["is_active"], name="school_libr_is_acti_2209c3_idx")),
        migrations.AddIndex(model_name="libraryissue", index=models.Index(fields=["issue_date"], name="school_libr_issue_d_c3b8e9_idx")),
        migrations.AddIndex(model_name="libraryissue", index=models.Index(fields=["due_date"], name="school_libr_due_dat_a314c7_idx")),
        migrations.AddIndex(model_name="libraryissue", index=models.Index(fields=["status"], name="school_libr_status_7cef13_idx")),
        migrations.AddIndex(model_name="libraryissue", index=models.Index(fields=["student", "status"], name="school_libr_student_2070e6_idx")),
    ]
