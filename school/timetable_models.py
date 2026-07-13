from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .models import AcademicClass, Staff, Subject


class WeeklyTimetableSlot(models.Model):
    """Day-wise class period assignment for timetable teacher mapping."""

    class Weekday(models.IntegerChoices):
        MONDAY = 1, "Monday"
        TUESDAY = 2, "Tuesday"
        WEDNESDAY = 3, "Wednesday"
        THURSDAY = 4, "Thursday"
        FRIDAY = 5, "Friday"
        SATURDAY = 6, "Saturday"
        SUNDAY = 7, "Sunday"

    academic_class = models.ForeignKey(
        AcademicClass,
        on_delete=models.CASCADE,
        related_name="weekly_timetable_slots",
    )
    day_of_week = models.PositiveSmallIntegerField(choices=Weekday.choices, default=Weekday.MONDAY)
    period_number = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Period number in the selected day. Example: 1 to 7.",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="weekly_timetable_slots",
    )
    teacher = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="weekly_timetable_slots",
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=80, blank=True)
    is_break = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_weekly_timetable_slots",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["academic_class__level_order", "academic_class__class_label", "day_of_week", "period_number", "start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["academic_class", "day_of_week", "period_number"],
                name="unique_class_day_period_slot",
            ),
            models.UniqueConstraint(
                fields=["teacher", "day_of_week", "period_number"],
                condition=models.Q(status=True, is_break=False, teacher__isnull=False),
                name="unique_teacher_day_period_slot",
            ),
        ]
        indexes = [
            models.Index(fields=["academic_class", "day_of_week", "period_number"], name="tt_slot_class_day_period_idx"),
            models.Index(fields=["teacher", "day_of_week", "start_time"], name="tt_slot_teacher_day_time_idx"),
            models.Index(fields=["subject", "day_of_week"], name="tt_slot_subject_day_idx"),
            models.Index(fields=["status", "day_of_week"], name="tt_slot_status_day_idx"),
        ]

    @property
    def time_range_display(self):
        if self.start_time and self.end_time:
            return f"{self.start_time.strftime('%I:%M %p').lstrip('0')} - {self.end_time.strftime('%I:%M %p').lstrip('0')}"
        return "-"

    @property
    def period_label(self):
        return f"P{self.period_number}"

    def clean(self):
        super().clean()
        errors = {}

        if self.start_time and self.end_time and self.end_time <= self.start_time:
            errors["end_time"] = "End time must be after start time."

        if self.status and not self.is_break:
            if not self.subject_id:
                errors["subject"] = "Subject is required for a teaching period."
            if not self.teacher_id:
                errors["teacher"] = "Teacher is required for a teaching period."

        can_check_overlap = self.day_of_week and self.start_time and self.end_time and self.status
        if can_check_overlap:
            class_overlaps = WeeklyTimetableSlot.objects.filter(
                academic_class_id=self.academic_class_id,
                day_of_week=self.day_of_week,
                status=True,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            ).exclude(pk=self.pk)
            if class_overlaps.exists():
                errors["start_time"] = "This class already has another period in this time range."

        if can_check_overlap and not self.is_break and self.teacher_id:
            teacher_overlaps = WeeklyTimetableSlot.objects.filter(
                teacher_id=self.teacher_id,
                day_of_week=self.day_of_week,
                status=True,
                is_break=False,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            ).exclude(pk=self.pk)
            if teacher_overlaps.exists():
                errors["teacher"] = "This teacher is already assigned to another class in this time range."

        if can_check_overlap and self.room:
            room_overlaps = WeeklyTimetableSlot.objects.filter(
                room__iexact=self.room.strip(),
                day_of_week=self.day_of_week,
                status=True,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            ).exclude(pk=self.pk)
            if room_overlaps.exists():
                errors["room"] = "This room is already assigned in this time range."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.room:
            self.room = self.room.strip()
        if not self.room and self.academic_class_id and self.academic_class and self.academic_class.room:
            self.room = self.academic_class.room
        super().save(*args, **kwargs)

    def __str__(self):
        label = "Break" if self.is_break else f"{self.subject} / {self.teacher}"
        return f"{self.academic_class} - {self.get_day_of_week_display()} {self.period_label}: {label}"
