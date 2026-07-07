from django.conf import settings
from django.db import models
from django.utils import timezone


class StaffLectureSession(models.Model):
    session_date = models.DateField(default=timezone.localdate)
    title = models.CharField(max_length=160, default="Daily Staff Lecture Attendance")
    note = models.TextField(blank=True)
    taken_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="taken_staff_lecture_sessions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["-session_date", "-created_at"]
        indexes = [models.Index(fields=["session_date"], name="school_staf_session_c7b9d1_idx")]

    def __str__(self):
        return f"{self.title} - {self.session_date}"


class StaffLectureAttendance(models.Model):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    LEAVE = "leave"
    STATUS_CHOICES = [
        (PRESENT, "Present"),
        (ABSENT, "Absent"),
        (LATE, "Late"),
        (LEAVE, "Leave"),
    ]

    session = models.ForeignKey(
        StaffLectureSession,
        on_delete=models.CASCADE,
        related_name="records",
    )
    staff = models.ForeignKey(
        "school.Staff",
        on_delete=models.CASCADE,
        related_name="lecture_attendance_records",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PRESENT)
    lecture_title = models.CharField(max_length=160, blank=True)
    remarks = models.CharField(max_length=255, blank=True)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="marked_staff_lecture_attendance",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["staff__name"]
        constraints = [
            models.UniqueConstraint(fields=["session", "staff"], name="unique_staff_lecture_attendance"),
        ]
        indexes = [
            models.Index(fields=["status"], name="school_staf_status_c25966_idx"),
            models.Index(fields=["staff", "status"], name="school_staf_staff_i_5d46f4_idx"),
        ]

    def __str__(self):
        return f"{self.staff.name}: {self.status} ({self.session.session_date})"
