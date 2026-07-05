from django.conf import settings
from django.db import models
from django.utils import timezone


class Notice(models.Model):
    AUDIENCE_ALL = "all"
    AUDIENCE_STUDENTS = "students"
    AUDIENCE_PARENTS = "parents"
    AUDIENCE_TEACHERS = "teachers"
    AUDIENCE_STAFF = "staff"

    AUDIENCE_CHOICES = [
        (AUDIENCE_ALL, "All"),
        (AUDIENCE_STUDENTS, "Students"),
        (AUDIENCE_PARENTS, "Parents"),
        (AUDIENCE_TEACHERS, "Teachers"),
        (AUDIENCE_STAFF, "Staff"),
    ]

    PRIORITY_NORMAL = "normal"
    PRIORITY_IMPORTANT = "important"
    PRIORITY_URGENT = "urgent"

    PRIORITY_CHOICES = [
        (PRIORITY_NORMAL, "Normal"),
        (PRIORITY_IMPORTANT, "Important"),
        (PRIORITY_URGENT, "Urgent"),
    ]

    title = models.CharField(max_length=220)
    body = models.TextField()
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default=AUDIENCE_ALL)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_NORMAL)
    publish_date = models.DateField(default=timezone.localdate)
    expiry_date = models.DateField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_notices",
    )
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["-publish_date", "-created_at"]
        indexes = [
            models.Index(fields=["publish_date"]),
            models.Index(fields=["audience"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["is_published"]),
        ]

    @property
    def is_expired(self):
        return bool(self.expiry_date and self.expiry_date < timezone.localdate())

    def __str__(self):
        return self.title
