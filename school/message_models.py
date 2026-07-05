from django.conf import settings
from django.db import models
from django.utils import timezone


class MessageThread(models.Model):
    PRIORITY_NORMAL = "normal"
    PRIORITY_IMPORTANT = "important"
    PRIORITY_URGENT = "urgent"

    PRIORITY_CHOICES = [
        (PRIORITY_NORMAL, "Normal"),
        (PRIORITY_IMPORTANT, "Important"),
        (PRIORITY_URGENT, "Urgent"),
    ]

    subject = models.CharField(max_length=240)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_message_threads",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_message_threads",
    )
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_NORMAL)
    is_read = models.BooleanField(default=False)
    is_archived_by_sender = models.BooleanField(default=False)
    is_archived_by_recipient = models.BooleanField(default=False)
    last_activity_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["-last_activity_at", "-created_at"]
        indexes = [
            models.Index(fields=["sender"]),
            models.Index(fields=["recipient"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["is_read"]),
            models.Index(fields=["last_activity_at"]),
        ]

    def __str__(self):
        return self.subject


class ThreadMessage(models.Model):
    thread = models.ForeignKey(
        MessageThread,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="written_thread_messages",
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "school"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["thread", "created_at"]),
            models.Index(fields=["author"]),
        ]

    def __str__(self):
        return f"{self.thread.subject} - {self.author}"
