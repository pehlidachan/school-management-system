from django import forms
from ..models import Gender, Grade, GuardianRelation, Student



class AddStudentForm(forms.ModelForm):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}))
    guardian_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    guardian_relation = forms.ModelChoiceField(queryset=GuardianRelation.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_enrollment = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    emergency_phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    previous_school = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), initial=True)
    
    class Meta:
        model = Student
        fields = ('__all__')
