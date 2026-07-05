from datetime import datetime
from decimal import Decimal

from django.shortcuts import render
from django.utils import timezone

from .access_control import finance_required
from .finance_models import FeeInvoice, SchoolExpense


def _date_or_none(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


@finance_required
def finance_summary_report(request):
    date_from_raw = request.GET.get("date_from") or ""
    date_to_raw = request.GET.get("date_to") or ""
    date_from = _date_or_none(date_from_raw)
    date_to = _date_or_none(date_to_raw)

    invoices = FeeInvoice.objects.select_related("student", "student__grade")
    paid_invoices = invoices.exclude(paid_at__isnull=True)
    expenses = SchoolExpense.objects.select_related("category")

    if date_from:
        invoices = invoices.filter(due_date__gte=date_from)
        paid_invoices = paid_invoices.filter(paid_at__gte=date_from)
        expenses = expenses.filter(payment_date__gte=date_from)
    if date_to:
        invoices = invoices.filter(due_date__lte=date_to)
        paid_invoices = paid_invoices.filter(paid_at__lte=date_to)
        expenses = expenses.filter(payment_date__lte=date_to)

    invoice_list = list(invoices[:500])
    paid_invoice_list = list(paid_invoices[:500])
    expense_list = list(expenses.order_by("-payment_date", "-created_at")[:500])

    total_invoiced = sum((invoice.net_total for invoice in invoice_list), Decimal("0"))
    total_collected = sum((invoice.amount_paid or Decimal("0") for invoice in paid_invoice_list), Decimal("0"))
    total_balance = sum((invoice.balance_due for invoice in invoice_list), Decimal("0"))
    total_expenses = sum((expense.amount or Decimal("0") for expense in expense_list), Decimal("0"))
    net_cash = total_collected - total_expenses

    return render(request, "finance_summary_report.html", {
        "date_from": date_from_raw,
        "date_to": date_to_raw,
        "total_invoiced": total_invoiced,
        "total_collected": total_collected,
        "total_balance": total_balance,
        "total_expenses": total_expenses,
        "net_cash": net_cash,
        "invoice_count": len(invoice_list),
        "paid_invoice_count": len(paid_invoice_list),
        "expense_count": len(expense_list),
        "recent_invoices": invoice_list[:12],
        "recent_expenses": expense_list[:12],
        "print_date": timezone.localdate(),
    })
