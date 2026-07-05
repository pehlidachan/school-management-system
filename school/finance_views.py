from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access_control import finance_required
from .finance_models import ExpenseCategory, FeeInvoice, SchoolExpense
from .models import Student


def _money(value, default="0"):
    try:
        return Decimal(str(value or default))
    except (InvalidOperation, ValueError):
        return Decimal(default)


def _date(value):
    if not value:
        return timezone.localdate()
    try:
        return timezone.datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return timezone.localdate()


def _refresh_overdue():
    today = timezone.localdate()
    FeeInvoice.objects.filter(status=FeeInvoice.PENDING, due_date__lt=today, amount_paid=0).update(status=FeeInvoice.OVERDUE)


@finance_required
def finance_dashboard(request):
    _refresh_overdue()
    invoices = FeeInvoice.objects.select_related("student", "student__grade")
    expenses = SchoolExpense.objects.select_related("category")
    total_invoiced = sum((invoice.net_total for invoice in invoices), Decimal("0"))
    total_paid = invoices.aggregate(total=Sum("amount_paid"))["total"] or Decimal("0")
    pending_balance = sum((invoice.balance_due for invoice in invoices.exclude(status=FeeInvoice.PAID)), Decimal("0"))
    total_expenses = expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0")
    context = {
        "total_invoiced": total_invoiced,
        "total_paid": total_paid,
        "pending_balance": pending_balance,
        "total_expenses": total_expenses,
        "recent_invoices": invoices[:8],
        "recent_expenses": expenses[:8],
    }
    return render(request, "finance_dashboard.html", context)


@finance_required
def fees_collection(request):
    _refresh_overdue()
    invoices = FeeInvoice.objects.select_related("student", "student__grade")[:100]
    return render(request, "fees_collection.html", {"invoices": invoices})


@finance_required
def add_fee_invoice(request):
    students = Student.objects.filter(status=True).select_related("grade").order_by("name")
    if request.method == "POST":
        student = get_object_or_404(Student, id=request.POST.get("student"))
        invoice = FeeInvoice.objects.create(
            student=student,
            title=(request.POST.get("title") or "Monthly Fee").strip(),
            billing_month=(request.POST.get("billing_month") or "").strip(),
            due_date=_date(request.POST.get("due_date")),
            tuition_fee=_money(request.POST.get("tuition_fee")),
            activities_fee=_money(request.POST.get("activities_fee")),
            miscellaneous_fee=_money(request.POST.get("miscellaneous_fee")),
            discount=_money(request.POST.get("discount")),
            fine=_money(request.POST.get("fine")),
            amount_paid=_money(request.POST.get("amount_paid")),
            payment_method=(request.POST.get("payment_method") or "").strip(),
            note=(request.POST.get("note") or "").strip(),
            created_by=request.user,
        )
        invoice.refresh_status(save=True)
        messages.success(request, "Fee invoice created successfully.")
        return redirect("fees_collection")
    return render(request, "fee_invoice_form.html", {"students": students, "today": timezone.localdate()})


@finance_required
def mark_fee_paid(request, invoice_id):
    invoice = get_object_or_404(FeeInvoice, id=invoice_id)
    if request.method != "POST":
        return redirect("fees_collection")
    amount = _money(request.POST.get("amount_paid"), default=str(invoice.net_total))
    invoice.amount_paid = min(amount, invoice.net_total)
    invoice.payment_method = (request.POST.get("payment_method") or invoice.payment_method or "Cash").strip()
    invoice.paid_at = timezone.localdate()
    invoice.refresh_status(save=True)
    messages.success(request, "Fee payment updated.")
    return redirect("fees_collection")


@finance_required
def school_expenses(request):
    expenses = SchoolExpense.objects.select_related("category")[:100]
    return render(request, "school_expenses.html", {"expenses": expenses})


@finance_required
def add_school_expense(request):
    categories = ExpenseCategory.objects.filter(status=True).order_by("name")
    if request.method == "POST":
        category_name = (request.POST.get("category_name") or "General").strip()
        category, _ = ExpenseCategory.objects.get_or_create(name=category_name)
        SchoolExpense.objects.create(
            category=category,
            title=(request.POST.get("title") or "Expense").strip(),
            quantity=(request.POST.get("quantity") or "").strip(),
            amount=_money(request.POST.get("amount")),
            payment_date=_date(request.POST.get("payment_date")),
            paid_to=(request.POST.get("paid_to") or "").strip(),
            payment_method=(request.POST.get("payment_method") or "Cash").strip(),
            note=(request.POST.get("note") or "").strip(),
            created_by=request.user,
        )
        messages.success(request, "School expense added successfully.")
        return redirect("school_expenses")
    return render(request, "school_expense_form.html", {"categories": categories, "today": timezone.localdate()})
