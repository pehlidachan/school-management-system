from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access_control import finance_required
from .ledger_models import CashBankAccount, CashBankTransaction, Vendor, VendorLedgerEntry


def _money(value, default="0"):
    try:
        return Decimal(str(value or default))
    except (InvalidOperation, ValueError):
        return Decimal(default)


@finance_required
def ledger_dashboard(request):
    vendors = Vendor.objects.filter(status=True)[:50]
    accounts = CashBankAccount.objects.filter(status=True)[:50]
    vendor_debit = VendorLedgerEntry.objects.aggregate(total=Sum("debit"))["total"] or Decimal("0")
    vendor_credit = VendorLedgerEntry.objects.aggregate(total=Sum("credit"))["total"] or Decimal("0")
    cash_income = CashBankTransaction.objects.filter(transaction_type=CashBankTransaction.INCOME).aggregate(total=Sum("amount"))["total"] or Decimal("0")
    cash_expense = CashBankTransaction.objects.exclude(transaction_type=CashBankTransaction.INCOME).aggregate(total=Sum("amount"))["total"] or Decimal("0")
    return render(request, "ledger_dashboard.html", {
        "vendors": vendors,
        "accounts": accounts,
        "vendor_balance": vendor_debit - vendor_credit,
        "cash_balance": cash_income - cash_expense,
    })


@finance_required
def add_vendor(request):
    if request.method == "POST":
        Vendor.objects.create(
            name=(request.POST.get("name") or "Vendor").strip(),
            phone=(request.POST.get("phone") or "").strip(),
            address=(request.POST.get("address") or "").strip(),
            note=(request.POST.get("note") or "").strip(),
        )
        messages.success(request, "Vendor added successfully.")
        return redirect("ledger_dashboard")
    return render(request, "vendor_form.html")


@finance_required
def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == "POST":
        VendorLedgerEntry.objects.create(
            vendor=vendor,
            entry_date=request.POST.get("entry_date") or timezone.localdate(),
            description=(request.POST.get("description") or "Ledger Entry").strip(),
            debit=_money(request.POST.get("debit")),
            credit=_money(request.POST.get("credit")),
            payment_method=(request.POST.get("payment_method") or "").strip(),
            note=(request.POST.get("note") or "").strip(),
            created_by=request.user,
        )
        messages.success(request, "Vendor ledger entry added.")
        return redirect("vendor_detail", vendor_id=vendor.id)
    entries = vendor.ledger_entries.all()[:200]
    balance = sum((entry.balance_effect for entry in entries), Decimal("0"))
    return render(request, "vendor_detail.html", {"vendor": vendor, "entries": entries, "balance": balance, "today": timezone.localdate()})


@finance_required
def cashbook(request):
    accounts = CashBankAccount.objects.filter(status=True)
    transactions = CashBankTransaction.objects.select_related("account", "created_by")[:200]
    if request.method == "POST":
        account_id = request.POST.get("account")
        if not account_id:
            account = CashBankAccount.objects.create(name="Main Cash", account_type=CashBankAccount.CASH)
        else:
            account = get_object_or_404(CashBankAccount, id=account_id)
        CashBankTransaction.objects.create(
            account=account,
            transaction_date=request.POST.get("transaction_date") or timezone.localdate(),
            title=(request.POST.get("title") or "Cashbook Entry").strip(),
            transaction_type=request.POST.get("transaction_type") or CashBankTransaction.EXPENSE,
            amount=_money(request.POST.get("amount")),
            note=(request.POST.get("note") or "").strip(),
            created_by=request.user,
        )
        messages.success(request, "Cashbook transaction added.")
        return redirect("cashbook")
    return render(request, "cashbook.html", {"accounts": accounts, "transactions": transactions, "today": timezone.localdate()})


@finance_required
def add_cash_bank_account(request):
    if request.method == "POST":
        CashBankAccount.objects.create(
            name=(request.POST.get("name") or "Cash Account").strip(),
            account_type=request.POST.get("account_type") or CashBankAccount.CASH,
            opening_balance=_money(request.POST.get("opening_balance")),
        )
        messages.success(request, "Cash/bank account added.")
        return redirect("cashbook")
    return render(request, "cash_bank_account_form.html", {"account_choices": CashBankAccount.ACCOUNT_CHOICES})
