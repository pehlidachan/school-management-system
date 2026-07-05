from django import forms
from ..models import Grade


class AddGradeForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'autofocus': True}))
    class Meta:
        model = Grade
        fields = ('id', 'name')