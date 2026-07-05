from django import forms
from ..models import Subject


class AddSubjectForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'autofocus': True}))
    class Meta:
        model = Subject
        fields = ('id', 'name')