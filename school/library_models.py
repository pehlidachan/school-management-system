from django.conf import settings
from django.db import models
from django.utils import timezone


class LibraryBook(models.Model):
    title = models.CharField(max_length=240)
    author = models.CharField(max_length=180, blank=True)
    isbn = models.CharField(max_length=80, blank=True)
    accession_number = models.CharField(max_length=80, unique=True)
    category = models.CharField(max_length=120, blank=True)
    publisher = models.CharField(max_length=180, blank=True)
    shelf_location = models.CharField(max_length=120, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="added_library_books",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["title", "author"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["isbn"]),
            models.Index(fields=["accession_number"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active"]),
        ]

    @property
    def issued_copies(self):
        return max((self.total_copies or 0) - (self.available_copies or 0), 0)

    def __str__(self):
        return f"{self.title} ({self.accession_number})"


class LibraryIssue(models.Model):
    ISSUED = "issued"
    RETURNED = "returned"
    OVERDUE = "overdue"

    STATUS_CHOICES = [
        (ISSUED, "Issued"),
        (RETURNED, "Returned"),
        (OVERDUE, "Overdue"),
    ]

    book = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    student = models.ForeignKey(
        "school.Student",
        on_delete=models.CASCADE,
        related_name="library_issues",
    )
    issue_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ISSUED)
    remarks = models.CharField(max_length=255, blank=True)
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issued_library_books",
    )
    returned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="returned_library_books",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["-issue_date", "-created_at"]
        indexes = [
            models.Index(fields=["issue_date"]),
            models.Index(fields=["due_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["student", "status"]),
        ]

    @property
    def is_overdue(self):
        return self.status == self.ISSUED and self.due_date < timezone.localdate()

    def refresh_status(self, save=False):
        if self.return_date:
            self.status = self.RETURNED
        elif self.due_date < timezone.localdate():
            self.status = self.OVERDUE
        else:
            self.status = self.ISSUED
        if save:
            self.save(update_fields=["status", "updated_at"])
        return self.status

    def __str__(self):
        return f"{self.book.title} -> {self.student.name} ({self.status})"
