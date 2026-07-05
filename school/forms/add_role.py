from django import forms
from ..models import Role


class AddRoleForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'autofocus': True}))
    class Meta:
        model = Role
        fields = ('id', 'name')