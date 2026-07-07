from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Vendor(models.Model):
    name = models.CharField(max_length=180)
    phone = models.CharField(max_length=80, blank=True)
    address = models.CharField(max_length=255, blank=True)
    note = models.TextField(blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "school"
        ordering = ["name"]
        indexes = [models.Index(fields=["status"], name="school_vend_status_9b1627_idx")]

    def __str__(self):
        return self.name


class VendorLedgerEntry(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="ledger_entries")
    entry_date = models.DateField(default=timezone.localdate)
    description = models.CharField(max_length=220)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=80, blank=True)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_vendor_ledger_entries")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "school"
        ordering = ["-entry_date", "-created_at"]
        indexes = [
            models.Index(fields=["entry_date"], name="school_vend_entry_d_06a5ef_idx"),
            models.Index(fields=["vendor", "entry_date"], name="school_vend_vendor__79d79e_idx"),
        ]

    @property
    def balance_effect(self):
        return Decimal(self.debit or 0) - Decimal(self.credit or 0)

    def __str__(self):
        return f"{self.vendor} - {self.description}"


class CashBankAccount(models.Model):
    CASH = "cash"
    BANK = "bank"
    ACCOUNT_CHOICES = [(CASH, "Cash"), (BANK, "Bank")]

    name = models.CharField(max_length=160)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_CHOICES, default=CASH)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "school"
        ordering = ["account_type", "name"]
        indexes = [
            models.Index(fields=["account_type"], name="school_cash_account_70f2e9_idx"),
            models.Index(fields=["status"], name="school_cash_status_e79a40_idx"),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"


class CashBankTransaction(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    TYPE_CHOICES = [(INCOME, "Income"), (EXPENSE, "Expense"), (TRANSFER, "Transfer")]

    account = models.ForeignKey(CashBankAccount, on_delete=models.CASCADE, related_name="transactions")
    transaction_date = models.DateField(default=timezone.localdate)
    title = models.CharField(max_length=180)
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=EXPENSE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_cash_bank_transactions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "school"
        ordering = ["-transaction_date", "-created_at"]
        indexes = [
            models.Index(fields=["transaction_date"], name="school_cash_transac_3fb9bb_idx"),
            models.Index(fields=["account", "transaction_type"], name="school_cash_account_e9f9ee_idx"),
        ]

    @property
    def signed_amount(self):
        amount = Decimal(self.amount or 0)
        return amount if self.transaction_type == self.INCOME else -amount

    def __str__(self):
        return f"{self.account} - {self.title}"
