from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class FeeInvoice(models.Model):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    PARTIAL = "partial"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PAID, "Paid"),
        (OVERDUE, "Overdue"),
        (PARTIAL, "Partial"),
    ]

    student = models.ForeignKey(
        "school.Student",
        on_delete=models.CASCADE,
        related_name="fee_invoices",
    )
    title = models.CharField(max_length=180, default="Monthly Fee")
    billing_month = models.CharField(max_length=30, blank=True)
    due_date = models.DateField()
    tuition_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    activities_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    miscellaneous_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fine = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    paid_at = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=80, blank=True)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_fee_invoices",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["-due_date", "student__name"]
        indexes = [
            models.Index(fields=["due_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["student", "status"]),
        ]

    @property
    def gross_total(self):
        return (self.tuition_fee or Decimal("0")) + (self.activities_fee or Decimal("0")) + (self.miscellaneous_fee or Decimal("0")) + (self.fine or Decimal("0"))

    @property
    def net_total(self):
        total = self.gross_total - (self.discount or Decimal("0"))
        return max(total, Decimal("0"))

    @property
    def balance_due(self):
        return max(self.net_total - (self.amount_paid or Decimal("0")), Decimal("0"))

    def refresh_status(self, save=False):
        if self.amount_paid >= self.net_total:
            self.status = self.PAID
            if not self.paid_at:
                self.paid_at = timezone.localdate()
        elif self.amount_paid > 0:
            self.status = self.PARTIAL
        elif self.due_date < timezone.localdate():
            self.status = self.OVERDUE
        else:
            self.status = self.PENDING
        if save:
            self.save(update_fields=["status", "paid_at", "updated_at"])
        return self.status

    def __str__(self):
        return f"{self.student.name} - {self.title} - {self.status}"


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    status = models.BooleanField(default=True)

    class Meta:
        app_label = "school"
        ordering = ["name"]

    def __str__(self):
        return self.name


class SchoolExpense(models.Model):
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )
    title = models.CharField(max_length=180)
    quantity = models.CharField(max_length=80, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(default=timezone.localdate)
    paid_to = models.CharField(max_length=180, blank=True)
    payment_method = models.CharField(max_length=80, blank=True)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_school_expenses",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["-payment_date", "-created_at"]
        indexes = [
            models.Index(fields=["payment_date"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.amount}"
