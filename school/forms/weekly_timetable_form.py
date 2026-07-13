from django import forms

from ..models import AcademicClass, Staff, Subject
from ..timetable_models import WeeklyTimetableSlot


class WeeklyTimetableSlotForm(forms.ModelForm):
    class Meta:
        model = WeeklyTimetableSlot
        fields = (
            "academic_class",
            "day_of_week",
            "period_number",
            "is_break",
            "subject",
            "teacher",
            "start_time",
            "end_time",
            "room",
            "status",
            "note",
        )
        widgets = {
            "academic_class": forms.Select(attrs={"class": "form-control"}),
            "day_of_week": forms.Select(attrs={"class": "form-control"}),
            "period_number": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 12}),
            "is_break": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "subject": forms.Select(attrs={"class": "form-control"}),
            "teacher": forms.Select(attrs={"class": "form-control"}),
            "start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "room": forms.TextInput(attrs={"class": "form-control", "placeholder": "Room / Lab / Ground"}),
            "status": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "note": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional note"}),
        }
        labels = {
            "academic_class": "Academic Class",
            "day_of_week": "Day",
            "period_number": "Period No.",
            "is_break": "Break / Free Period",
            "start_time": "Start Time",
            "end_time": "End Time",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["academic_class"].queryset = AcademicClass.objects.filter(status=True).select_related("academic_session", "grade").order_by("academic_session__name", "level_order", "grade__name", "section")
        self.fields["subject"].queryset = Subject.objects.all().order_by("name")
        self.fields["teacher"].queryset = Staff.objects.filter(status=True).select_related("role", "subject").order_by("name")
        self.fields["subject"].required = False
        self.fields["teacher"].required = False
        self.fields["room"].required = False
        self.fields["note"].required = False

    def clean(self):
        cleaned = super().clean()
        is_break = cleaned.get("is_break")
        status = cleaned.get("status")
        subject = cleaned.get("subject")
        teacher = cleaned.get("teacher")

        if status and not is_break:
            if not subject:
                self.add_error("subject", "Subject is required for a teaching period.")
            if not teacher:
                self.add_error("teacher", "Teacher is required for a teaching period.")
        return cleaned
