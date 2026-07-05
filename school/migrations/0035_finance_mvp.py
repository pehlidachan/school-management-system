# Generated manually for Phase 2.4 Finance MVP

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("school", "0034_attendance_mvp"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExpenseCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("status", models.BooleanField(default=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="FeeInvoice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="Monthly Fee", max_length=180)),
                ("billing_month", models.CharField(blank=True, max_length=30)),
                ("due_date", models.DateField()),
                ("tuition_fee", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("activities_fee", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("miscellaneous_fee", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("discount", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("fine", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("amount_paid", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("paid", "Paid"), ("overdue", "Overdue"), ("partial", "Partial")], default="pending", max_length=20)),
                ("paid_at", models.DateField(blank=True, null=True)),
                ("payment_method", models.CharField(blank=True, max_length=80)),
                ("note", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_fee_invoices", to=settings.AUTH_USER_MODEL)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="fee_invoices", to="school.student")),
            ],
            options={"ordering": ["-due_date", "student__name"]},
        ),
        migrations.CreateModel(
            name="SchoolExpense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("quantity", models.CharField(blank=True, max_length=80)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("payment_date", models.DateField(default=django.utils.timezone.localdate)),
                ("paid_to", models.CharField(blank=True, max_length=180)),
                ("payment_method", models.CharField(blank=True, max_length=80)),
                ("note", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="expenses", to="school.expensecategory")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_school_expenses", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-payment_date", "-created_at"]},
        ),
        migrations.AddIndex(model_name="feeinvoice", index=models.Index(fields=["due_date"], name="school_feei_due_dat_d18f46_idx")),
        migrations.AddIndex(model_name="feeinvoice", index=models.Index(fields=["status"], name="school_feei_status_825db3_idx")),
        migrations.AddIndex(model_name="feeinvoice", index=models.Index(fields=["student", "status"], name="school_feei_student_7596ad_idx")),
        migrations.AddIndex(model_name="schoolexpense", index=models.Index(fields=["payment_date"], name="school_scho_payment_562553_idx")),
        migrations.AddIndex(model_name="schoolexpense", index=models.Index(fields=["category"], name="school_scho_categor_ba76ac_idx")),
    ]
