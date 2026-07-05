from django.conf import settings
from django.db import models
from django.utils import timezone


class SchoolCalendarEvent(models.Model):
    TYPE_EVENT = "event"
    TYPE_HOLIDAY = "holiday"
    TYPE_EXAM = "exam"
    TYPE_MEETING = "meeting"
    TYPE_DEADLINE = "deadline"

    EVENT_TYPE_CHOICES = [
        (TYPE_EVENT, "Event"),
        (TYPE_HOLIDAY, "Holiday"),
        (TYPE_EXAM, "Exam"),
        (TYPE_MEETING, "Meeting"),
        (TYPE_DEADLINE, "Deadline"),
    ]

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

    title = models.CharField(max_length=220)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default=TYPE_EVENT)
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default=AUDIENCE_ALL)
    event_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=220, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_calendar_events",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["event_date", "start_time", "title"]
        indexes = [
            models.Index(fields=["event_date"]),
            models.Index(fields=["event_type"]),
            models.Index(fields=["audience"]),
            models.Index(fields=["is_active"]),
        ]

    @property
    def is_past(self):
        end = self.end_date or self.event_date
        return end < timezone.localdate()

    def __str__(self):
        return f"{self.event_date} - {self.title}"
