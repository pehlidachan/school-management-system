from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class Exam(models.Model):
    name = models.CharField(max_length=180)
    grade = models.ForeignKey(
        "school.Grade",
        on_delete=models.CASCADE,
        related_name="exams",
    )
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_exams",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["-start_date", "grade__name", "name"]
        indexes = [
            models.Index(fields=["grade", "start_date"]),
            models.Index(fields=["is_published"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.grade}"


class ExamSubject(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="exam_subjects",
    )
    subject = models.ForeignKey(
        "school.Subject",
        on_delete=models.CASCADE,
        related_name="exam_subjects",
    )
    total_marks = models.DecimalField(max_digits=7, decimal_places=2, default=100)
    passing_marks = models.DecimalField(max_digits=7, decimal_places=2, default=33)

    class Meta:
        app_label = "school"
        ordering = ["subject__name"]
        constraints = [
            models.UniqueConstraint(fields=["exam", "subject"], name="unique_subject_per_exam"),
        ]

    def __str__(self):
        return f"{self.exam} - {self.subject}"


class StudentMark(models.Model):
    exam_subject = models.ForeignKey(
        ExamSubject,
        on_delete=models.CASCADE,
        related_name="marks",
    )
    student = models.ForeignKey(
        "school.Student",
        on_delete=models.CASCADE,
        related_name="exam_marks",
    )
    marks_obtained = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    remarks = models.CharField(max_length=255, blank=True)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="marked_exam_results",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["student__name"]
        constraints = [
            models.UniqueConstraint(fields=["exam_subject", "student"], name="unique_student_mark_per_exam_subject"),
        ]
        indexes = [
            models.Index(fields=["student"]),
            models.Index(fields=["exam_subject"]),
        ]

    @property
    def is_passed(self):
        return Decimal(self.marks_obtained or 0) >= Decimal(self.exam_subject.passing_marks or 0)

    def __str__(self):
        return f"{self.student.name} - {self.exam_subject.subject.name}: {self.marks_obtained}"
