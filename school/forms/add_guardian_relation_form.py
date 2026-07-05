from django import forms
from ..models import GuardianRelation


class AddGuardianRelationForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'autofocus': True}))
    class Meta:
        model = GuardianRelation
        fields = ('id', 'name')