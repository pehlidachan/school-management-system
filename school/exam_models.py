from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class Exam(models.Model):
    WEEKLY_TEST = "weekly_test"
    MONTHLY_TEST = "monthly_test"
    QUARTERLY_TEST = "quarterly_test"
    MID_TERM = "mid_term"
    PRE_FINAL = "pre_final"
    FINAL = "final"

    EXAM_TYPE_CHOICES = [
        (WEEKLY_TEST, "Weekly Test"),
        (MONTHLY_TEST, "Monthly Test"),
        (QUARTERLY_TEST, "Quarterly Test"),
        (MID_TERM, "Mid Term Exam"),
        (PRE_FINAL, "Pre Final Exam"),
        (FINAL, "Final Exam"),
    ]

    EXAM_SEQUENCE = {
        WEEKLY_TEST: 10,
        MONTHLY_TEST: 20,
        QUARTERLY_TEST: 30,
        MID_TERM: 40,
        PRE_FINAL: 50,
        FINAL: 60,
    }

    DEFAULT_WEIGHT = {
        WEEKLY_TEST: Decimal("5.00"),
        MONTHLY_TEST: Decimal("10.00"),
        QUARTERLY_TEST: Decimal("15.00"),
        MID_TERM: Decimal("25.00"),
        PRE_FINAL: Decimal("20.00"),
        FINAL: Decimal("25.00"),
    }

    name = models.CharField(max_length=180)
    exam_type = models.CharField(max_length=30, choices=EXAM_TYPE_CHOICES, default=MONTHLY_TEST)
    academic_year = models.CharField(max_length=20, default="2026")
    term_label = models.CharField(max_length=80, blank=True)
    grade = models.ForeignKey(
        "school.Grade",
        on_delete=models.CASCADE,
        related_name="exams",
    )
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)
    sequence = models.PositiveSmallIntegerField(default=20)
    result_weight = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    is_locked = models.BooleanField(default=False)
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
        ordering = ["academic_year", "grade__name", "sequence", "start_date", "name"]
        indexes = [
            models.Index(fields=["grade", "start_date"]),
            models.Index(fields=["academic_year", "grade", "exam_type"], name="exam_year_grade_type_idx"),
            models.Index(fields=["sequence"], name="exam_sequence_idx"),
            models.Index(fields=["is_published"]),
            models.Index(fields=["is_locked"], name="exam_locked_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["academic_year", "grade", "exam_type", "name"],
                name="unique_exam_schema_per_grade_year",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.sequence:
            self.sequence = self.EXAM_SEQUENCE.get(self.exam_type, 20)
        if self.result_weight in (None, Decimal("0"), 0):
            self.result_weight = self.DEFAULT_WEIGHT.get(self.exam_type, Decimal("10.00"))
        if not self.name:
            self.name = self.get_exam_type_display()
        super().save(*args, **kwargs)

    @property
    def is_major_exam(self):
        return self.exam_type in {self.MID_TERM, self.PRE_FINAL, self.FINAL}

    def __str__(self):
        return f"{self.get_exam_type_display()} - {self.grade} - {self.academic_year}"


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


class ExamDateSheetItem(models.Model):
    exam_subject = models.OneToOneField(
        ExamSubject,
        on_delete=models.CASCADE,
        related_name="date_sheet_item",
    )
    paper_date = models.DateField()
    start_time = models.TimeField(default="09:00")
    end_time = models.TimeField(default="12:00")
    room = models.CharField(max_length=80, blank=True)
    instructions = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        app_label = "school"
        ordering = ["paper_date", "start_time", "sort_order", "exam_subject__subject__name"]
        indexes = [
            models.Index(fields=["paper_date"], name="exam_datesheet_date_idx"),
            models.Index(fields=["sort_order"], name="exam_datesheet_order_idx"),
        ]

    def __str__(self):
        return f"{self.exam_subject.exam} - {self.exam_subject.subject} - {self.paper_date}"


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
