from decimal import Decimal

from django import forms

from ..models import Gender, Grade, GuardianRelation, Student


class AddStudentForm(forms.ModelForm):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gr_no = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GR / registration number'}))
    admission_no = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admission number'}))
    roll_no = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Class roll number'}))
    student_name_urdu = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}))
    father_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}))
    guardian_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    guardian_relation = forms.ModelChoiceField(queryset=GuardianRelation.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    guardian_cnic = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'xxxxx-xxxxxxx-x'}))
    address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_enrollment = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}))
    rejoining_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mother_mobile = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    whatsapp_no = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    emergency_phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    previous_school = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    blood_group = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fee_category = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    monthly_fee = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}))
    welcome_card_sent = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    status = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), initial=True, required=False)

    class Meta:
        model = Student
        exclude = ('photo_path', 'welcome_card_sent_at')

    def clean_monthly_fee(self):
        value = self.cleaned_data.get('monthly_fee')
        if value in (None, ''):
            return Decimal('0.00')
        return value
