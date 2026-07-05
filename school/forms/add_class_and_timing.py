from django import forms
from ..models import ClassAndTiming, Staff, Subject, Grade


class AddClassAndTimingForm(forms.ModelForm):
    class_name = forms.ModelChoiceField(queryset=Grade.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_one_subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_one_teacher = forms.ModelChoiceField(required=False, queryset=Staff.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_one_from = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_one_to = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_two_subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_two_teacher = forms.ModelChoiceField(required=False, queryset=Staff.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_two_from = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_two_to = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_three_subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_three_teacher = forms.ModelChoiceField(required=False, queryset=Staff.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_three_from = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_three_to = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_four_subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_four_teacher = forms.ModelChoiceField(required=False, queryset=Staff.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_four_from = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_four_to = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_five_subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_five_teacher = forms.ModelChoiceField(required=False, queryset=Staff.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_five_from = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_five_to = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_six_subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_six_teacher = forms.ModelChoiceField(required=False, queryset=Staff.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_six_from = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_six_to = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_seven_subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_seven_teacher = forms.ModelChoiceField(required=False, queryset=Staff.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    period_seven_from = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    period_seven_to = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type': 'time'}))
    status = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input'}), initial=True)


    class Meta():
        model = ClassAndTiming
        fields = ('__all__')