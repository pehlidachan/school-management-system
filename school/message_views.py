from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access_control import staff_required
from .message_models import MessageThread, ThreadMessage

User = get_user_model()


def _visible_threads(user):
    return MessageThread.objects.filter(Q(sender=user) | Q(recipient=user))


@staff_required
def message_inbox(request):
    threads = _visible_threads(request.user).select_related("sender", "recipient")[:100]
    unread_count = MessageThread.objects.filter(recipient=request.user, is_read=False).count()
    sent_count = MessageThread.objects.filter(sender=request.user).count()
    context = {
        "threads": threads,
        "unread_count": unread_count,
        "sent_count": sent_count,
        "total_threads": threads.count(),
    }
    return render(request, "message_inbox.html", context)


@staff_required
def compose_message(request):
    users = User.objects.filter(is_active=True).exclude(id=request.user.id).order_by("username")
    if request.method == "POST":
        recipient = get_object_or_404(User, id=request.POST.get("recipient"), is_active=True)
        subject = (request.POST.get("subject") or "").strip()
        body = (request.POST.get("body") or "").strip()
        if not subject or not body:
            messages.error(request, "Subject and message body are required.")
            return redirect("compose_message")
        thread = MessageThread.objects.create(
            subject=subject,
            sender=request.user,
            recipient=recipient,
            priority=request.POST.get("priority") or MessageThread.PRIORITY_NORMAL,
            last_activity_at=timezone.now(),
        )
        ThreadMessage.objects.create(thread=thread, author=request.user, body=body)
        messages.success(request, "Message sent successfully.")
        return redirect("message_detail", thread_id=thread.id)
    return render(request, "message_compose.html", {"users": users, "priority_choices": MessageThread.PRIORITY_CHOICES})


@staff_required
def message_detail(request, thread_id):
    thread = get_object_or_404(_visible_threads(request.user).select_related("sender", "recipient"), id=thread_id)
    if thread.recipient == request.user and not thread.is_read:
        thread.is_read = True
        thread.save(update_fields=["is_read", "updated_at"])
    thread_messages = thread.messages.select_related("author")
    return render(request, "message_detail.html", {"thread": thread, "thread_messages": thread_messages})


@staff_required
def reply_message(request, thread_id):
    thread = get_object_or_404(_visible_threads(request.user), id=thread_id)
    if request.method != "POST":
        return redirect("message_detail", thread_id=thread.id)
    body = (request.POST.get("body") or "").strip()
    if not body:
        messages.error(request, "Reply body is required.")
        return redirect("message_detail", thread_id=thread.id)
    ThreadMessage.objects.create(thread=thread, author=request.user, body=body)
    thread.last_activity_at = timezone.now()
    if request.user == thread.sender:
        thread.is_read = False
    thread.save(update_fields=["last_activity_at", "is_read", "updated_at"])
    messages.success(request, "Reply sent successfully.")
    return redirect("message_detail", thread_id=thread.id)
