from django import forms
from ..models import Staff, ClassAndTiming, ClassIncharge

class AddClassInchargeForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=Staff.objects.all(), widget=forms.Select(attrs={'class' : 'form-control'}))
    class_obj = forms.ModelChoiceField(queryset=ClassAndTiming.objects.all(), widget=forms.Select(attrs={'class' : 'form-control'}))
    class Meta:
        model = ClassIncharge
        fields = ('__all__')