from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .access_control import admin_required
from .forms.weekly_timetable_form import WeeklyTimetableSlotForm
from .models import AcademicClass
from .profile_settings_models import SchoolBrandProfile
from .timetable_models import WeeklyTimetableSlot


def _active_academic_classes():
    return AcademicClass.objects.filter(status=True).select_related("academic_session", "grade", "class_teacher").order_by("academic_session__name", "level_order", "grade__name", "section")


def _build_day_rows(slots):
    days = [
        {"value": value, "label": label, "slots": []}
        for value, label in WeeklyTimetableSlot.Weekday.choices
    ]
    day_map = {day["value"]: day for day in days}
    for slot in slots:
        if slot.day_of_week in day_map:
            day_map[slot.day_of_week]["slots"].append(slot)
    return days


@admin_required
def timetable_dashboard(request):
    classes = _active_academic_classes()
    selected_class = None
    class_id = request.GET.get("class_id")
    if class_id:
        selected_class = classes.filter(pk=class_id).first()
    if selected_class is None:
        selected_class = classes.first()

    slots = WeeklyTimetableSlot.objects.none()
    if selected_class:
        slots = WeeklyTimetableSlot.objects.filter(academic_class=selected_class).select_related("subject", "teacher", "academic_class").order_by("day_of_week", "period_number", "start_time")

    slot_list = list(slots)
    context = {
        "classes": classes,
        "selected_class": selected_class,
        "days": _build_day_rows(slot_list),
        "total_slots": len(slot_list),
        "active_slots": len([slot for slot in slot_list if slot.status]),
        "teacher_count": len({slot.teacher_id for slot in slot_list if slot.teacher_id}),
        "subject_count": len({slot.subject_id for slot in slot_list if slot.subject_id}),
    }
    return render(request, "timetable_dashboard.html", context)


@admin_required
def add_timetable_slot(request):
    initial = {
        "academic_class": request.GET.get("class_id") or None,
        "day_of_week": request.GET.get("day") or WeeklyTimetableSlot.Weekday.MONDAY,
        "period_number": request.GET.get("period") or 1,
    }
    if request.method == "POST":
        form = WeeklyTimetableSlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.created_by = request.user
            slot.save()
            messages.success(request, "Timetable period assigned successfully.")
            return redirect(f"{reverse('timetable_dashboard')}?class_id={slot.academic_class_id}")
        messages.error(request, "Please fix the timetable errors below.")
    else:
        form = WeeklyTimetableSlotForm(initial=initial)

    return render(request, "timetable_slot_form.html", {"form": form, "title": "Assign Timetable Period", "submit_label": "Save Period"})


@admin_required
def edit_timetable_slot(request, slot_id):
    slot = get_object_or_404(WeeklyTimetableSlot, pk=slot_id)
    if request.method == "POST":
        form = WeeklyTimetableSlotForm(request.POST, instance=slot)
        if form.is_valid():
            slot = form.save()
            messages.success(request, "Timetable period updated successfully.")
            return redirect(f"{reverse('timetable_dashboard')}?class_id={slot.academic_class_id}")
        messages.error(request, "Please fix the timetable errors below.")
    else:
        form = WeeklyTimetableSlotForm(instance=slot)

    return render(request, "timetable_slot_form.html", {"form": form, "slot": slot, "title": "Edit Timetable Period", "submit_label": "Update Period"})


@admin_required
@require_POST
def delete_timetable_slot(request, slot_id):
    slot = get_object_or_404(WeeklyTimetableSlot, pk=slot_id)
    class_id = slot.academic_class_id
    slot.delete()
    messages.success(request, "Timetable period deleted successfully.")
    return redirect(f"{reverse('timetable_dashboard')}?class_id={class_id}")


@admin_required
def timetable_print(request, class_id):
    academic_class = get_object_or_404(_active_academic_classes(), pk=class_id)
    slots = WeeklyTimetableSlot.objects.filter(academic_class=academic_class, status=True).select_related("subject", "teacher").order_by("day_of_week", "period_number", "start_time")
    brand = SchoolBrandProfile.objects.filter(is_active=True).first()
    context = {
        "brand": brand,
        "academic_class": academic_class,
        "days": _build_day_rows(list(slots)),
        "printed_on": timezone.localtime().date(),
    }
    return render(request, "timetable_print.html", context)
