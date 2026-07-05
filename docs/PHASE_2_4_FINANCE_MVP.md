# Phase 2.4 Finance MVP

This phase adds the first finance module for a sellable school ERP MVP.

## Access

Finance pages are limited to:

- Superuser
- School Admin
- Principal
- Accountant

## Added database tables

- `FeeInvoice`
  - Student fee invoice.
  - Tuition, activities, miscellaneous, discount, fine.
  - Paid amount, due date, status and payment method.
  - Status values: `pending`, `paid`, `partial`, `overdue`.

- `ExpenseCategory`
  - Expense category master data.

- `SchoolExpense`
  - School expense ledger.
  - Category, title, quantity, amount, payment date, paid to and method.

## Added pages

- `/finance/`
  - Finance dashboard.
  - Total invoiced, paid, pending balance and expenses.

- `/finance/fees/`
  - Fees collection list.
  - Mark invoice as paid.

- `/finance/fees/add/`
  - Add new fee invoice.

- `/finance/expenses/`
  - School expenses list.

- `/finance/expenses/add/`
  - Add new school expense.

## Notes

This is an MVP. Future upgrades can add:

- Fee receipt PDF.
- Installments.
- Monthly fee generation for full class.
- Fine auto-calculation.
- Discounts/scholarships.
- Parent/student fee view.
- CSV/Excel export.
- Streamlit finance analytics.

## Daily workflow

After pulling this update, run:

```powershell
git pull
.\start_server_windows.bat
```

Then open Finance from the sidebar.
