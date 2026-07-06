from datetime import datetime

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access_control import staff_required
from .notice_models import Notice


def _date_or_none(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


@staff_required
def notice_board(request):
    notices = Notice.objects.filter(is_published=True)[:100]
    featured_notice = notices.first()
    return render(request, "notice_board.html", {"notices": notices, "featured_notice": featured_notice})


@staff_required
def add_notice(request):
    if request.method == "POST":
        notice = Notice.objects.create(
            title=(request.POST.get("title") or "").strip(),
            body=(request.POST.get("body") or "").strip(),
            audience=request.POST.get("audience") or Notice.AUDIENCE_ALL,
            priority=request.POST.get("priority") or Notice.PRIORITY_NORMAL,
            publish_date=_date_or_none(request.POST.get("publish_date")) or timezone.localdate(),
            expiry_date=_date_or_none(request.POST.get("expiry_date")),
            is_published=bool(request.POST.get("is_published")),
            created_by=request.user,
        )
        if not notice.title or not notice.body:
            notice.delete()
            messages.error(request, "Notice title and body are required.")
            return redirect("add_notice")
        messages.success(request, "Notice published successfully.")
        return redirect("notice_board")

    context = {
        "today": timezone.localdate(),
        "audience_choices": Notice.AUDIENCE_CHOICES,
        "priority_choices": Notice.PRIORITY_CHOICES,
    }
    return render(request, "notice_form.html", context)


@staff_required
def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    Notice.objects.filter(id=notice.id).update(view_count=notice.view_count + 1)
    notice.view_count += 1
    related_notices = Notice.objects.filter(is_published=True).exclude(id=notice.id)[:5]
    return render(request, "notice_detail.html", {"notice": notice, "related_notices": related_notices})
