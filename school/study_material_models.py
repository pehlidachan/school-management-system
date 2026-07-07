from django.conf import settings
from django.db import models
from django.utils import timezone


class StudyMaterial(models.Model):
    title = models.CharField(max_length=180)
    grade = models.ForeignKey(
        "school.Grade",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="study_materials",
    )
    subject = models.ForeignKey(
        "school.Subject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="study_materials",
    )
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    external_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_study_materials",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["-created_at", "grade__name", "subject__name"]
        indexes = [
            models.Index(fields=["is_published"]),
            models.Index(fields=["grade", "subject"]),
        ]

    def __str__(self):
        return self.title
