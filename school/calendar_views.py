from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .access_control import staff_required
from .calendar_models import SchoolCalendarEvent


def _date_or_none(value):
    if not value:
        return None
    try:
        return timezone.datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _time_or_none(value):
    if not value:
        return None
    try:
        return timezone.datetime.strptime(value, "%H:%M").time()
    except ValueError:
        return None


@staff_required
def calendar_dashboard(request):
    today = timezone.localdate()
    upcoming_events = SchoolCalendarEvent.objects.filter(is_active=True, event_date__gte=today)[:20]
    past_events = SchoolCalendarEvent.objects.filter(is_active=True, event_date__lt=today).order_by("-event_date")[:10]
    today_events = SchoolCalendarEvent.objects.filter(is_active=True, event_date=today)
    context = {
        "today": today,
        "today_events": today_events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "total_upcoming": upcoming_events.count(),
        "total_today": today_events.count(),
    }
    return render(request, "calendar_dashboard.html", context)


@staff_required
def add_calendar_event(request):
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        if not title:
            messages.error(request, "Event title is required.")
            return redirect("add_calendar_event")

        SchoolCalendarEvent.objects.create(
            title=title,
            event_type=request.POST.get("event_type") or SchoolCalendarEvent.TYPE_EVENT,
            audience=request.POST.get("audience") or SchoolCalendarEvent.AUDIENCE_ALL,
            event_date=_date_or_none(request.POST.get("event_date")) or timezone.localdate(),
            end_date=_date_or_none(request.POST.get("end_date")),
            start_time=_time_or_none(request.POST.get("start_time")),
            end_time=_time_or_none(request.POST.get("end_time")),
            location=(request.POST.get("location") or "").strip(),
            description=(request.POST.get("description") or "").strip(),
            is_active=bool(request.POST.get("is_active")),
            created_by=request.user,
        )
        messages.success(request, "Calendar event saved successfully.")
        return redirect("calendar_dashboard")

    context = {
        "today": timezone.localdate(),
        "event_type_choices": SchoolCalendarEvent.EVENT_TYPE_CHOICES,
        "audience_choices": SchoolCalendarEvent.AUDIENCE_CHOICES,
    }
    return render(request, "calendar_event_form.html", context)


@staff_required
def calendar_event_detail(request, event_id):
    event = get_object_or_404(SchoolCalendarEvent, id=event_id)
    related_events = SchoolCalendarEvent.objects.filter(is_active=True).exclude(id=event.id)[:5]
    return render(request, "calendar_event_detail.html", {"event": event, "related_events": related_events})
