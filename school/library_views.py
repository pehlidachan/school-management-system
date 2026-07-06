from datetime import datetime

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access_control import staff_required
from .library_models import LibraryBook, LibraryIssue
from .models import Student


def _date_or_none(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _refresh_overdue():
    today = timezone.localdate()
    LibraryIssue.objects.filter(status=LibraryIssue.ISSUED, due_date__lt=today, return_date__isnull=True).update(status=LibraryIssue.OVERDUE)


@staff_required
def library_dashboard(request):
    _refresh_overdue()
    books = LibraryBook.objects.filter(is_active=True)
    active_issues = LibraryIssue.objects.select_related("book", "student").exclude(status=LibraryIssue.RETURNED)[:20]
    recent_returns = LibraryIssue.objects.select_related("book", "student").filter(status=LibraryIssue.RETURNED)[:10]
    context = {
        "books": books[:100],
        "active_issues": active_issues,
        "recent_returns": recent_returns,
        "total_books": books.count(),
        "total_copies": books.aggregate(total=Sum("total_copies"))["total"] or 0,
        "available_copies": books.aggregate(total=Sum("available_copies"))["total"] or 0,
        "issued_count": LibraryIssue.objects.exclude(status=LibraryIssue.RETURNED).count(),
    }
    return render(request, "library_dashboard.html", context)


@staff_required
def add_library_book(request):
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        accession_number = (request.POST.get("accession_number") or "").strip()
        if not title or not accession_number:
            messages.error(request, "Book title and accession number are required.")
            return redirect("add_library_book")
        total_copies = int(request.POST.get("total_copies") or 1)
        LibraryBook.objects.create(
            title=title,
            author=(request.POST.get("author") or "").strip(),
            isbn=(request.POST.get("isbn") or "").strip(),
            accession_number=accession_number,
            category=(request.POST.get("category") or "").strip(),
            publisher=(request.POST.get("publisher") or "").strip(),
            shelf_location=(request.POST.get("shelf_location") or "").strip(),
            total_copies=max(total_copies, 1),
            available_copies=max(total_copies, 1),
            is_active=bool(request.POST.get("is_active")),
            added_by=request.user,
        )
        messages.success(request, "Book added successfully.")
        return redirect("library_dashboard")
    return render(request, "library_book_form.html")


@staff_required
def issue_library_book(request):
    books = LibraryBook.objects.filter(is_active=True, available_copies__gt=0).order_by("title")
    students = Student.objects.filter(status=True).select_related("grade").order_by("name")
    if request.method == "POST":
        book = get_object_or_404(LibraryBook, id=request.POST.get("book"), is_active=True)
        student = get_object_or_404(Student, id=request.POST.get("student"), status=True)
        if book.available_copies <= 0:
            messages.error(request, "This book has no available copy.")
            return redirect("issue_library_book")
        due_date = _date_or_none(request.POST.get("due_date")) or timezone.localdate()
        LibraryIssue.objects.create(
            book=book,
            student=student,
            issue_date=_date_or_none(request.POST.get("issue_date")) or timezone.localdate(),
            due_date=due_date,
            remarks=(request.POST.get("remarks") or "").strip(),
            issued_by=request.user,
        )
        book.available_copies = max(book.available_copies - 1, 0)
        book.save(update_fields=["available_copies", "updated_at"])
        messages.success(request, "Book issued successfully.")
        return redirect("library_dashboard")
    return render(request, "library_issue_form.html", {"books": books, "students": students, "today": timezone.localdate()})


@staff_required
def return_library_book(request, issue_id):
    issue = get_object_or_404(LibraryIssue.objects.select_related("book"), id=issue_id)
    if request.method != "POST":
        return redirect("library_dashboard")
    if issue.status == LibraryIssue.RETURNED:
        messages.info(request, "This book is already returned.")
        return redirect("library_dashboard")
    issue.return_date = timezone.localdate()
    issue.status = LibraryIssue.RETURNED
    issue.returned_by = request.user
    issue.save(update_fields=["return_date", "status", "returned_by", "updated_at"])
    book = issue.book
    book.available_copies = min(book.available_copies + 1, book.total_copies)
    book.save(update_fields=["available_copies", "updated_at"])
    messages.success(request, "Book returned successfully.")
    return redirect("library_dashboard")
