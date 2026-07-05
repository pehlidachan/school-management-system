# Phase 2.8 Library MVP

This phase adds a SchoolHub-style library module.

## Added database tables

- `LibraryBook`
  - Title, author, ISBN, accession number.
  - Category, publisher, shelf location.
  - Total copies and available copies.
  - Active/inactive status.

- `LibraryIssue`
  - Book assigned to student.
  - Issue date, due date and return date.
  - Status: Issued, Returned, Overdue.
  - Issued by / returned by user.

## Added pages

- `/library/`
  - Library dashboard.
  - Book catalog.
  - Active book issues.
  - Return button.

- `/library/books/add/`
  - Add new library book.

- `/library/issue/`
  - Assign available book to a student.

- `/library/issue/<issue_id>/return/`
  - Mark book as returned.

## Access

Currently library pages use `staff_required`, so staff-side users can manage the library.

## Sidebar

The Library sidebar item now opens the real library page instead of a placeholder.

## Future upgrades

- Barcode/QR code labels.
- ISBN lookup.
- Staff borrowing.
- Fine calculation for overdue books.
- Student/parent read-only issued book view.
- Excel import/export for books.
