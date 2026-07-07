from django import forms
from django.db.models import Case, IntegerField, Value, When

from ..models import Staff, Gender, Role, Subject, EmploymentStatus
from ..constants import STAFF_ROLE_NAMES, DEFAULT_EMPLOYMENT_STATUS_NAMES


class AddStaffForm(forms.ModelForm):
    name = forms.CharField(max_length=75, widget=forms.TextInput(attrs={'class': 'form-control'}))
    staff_code = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Staff code'}))
    staff_name_urdu = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}))
    father_or_husband_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cnic = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'xxxxx-xxxxxxx-x'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type':'date'}))
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    qualification = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'})) 
    experience = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'})) 
    role = forms.ModelChoiceField(queryset=Role.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    whatsapp_no = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    emergency_phone = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    joining_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type':'date'}))
    rejoining_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type':'date'}))
    salary = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    employment_status = forms.ModelChoiceField(queryset=EmploymentStatus.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    contract_details = forms.CharField(max_length=1000, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    can_print_student_biodata = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    can_print_staff_biodata = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    birthday_card_sent = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    status = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), initial=True, required=False)

    class Meta:
        model = Staff
        exclude = ('photo_path',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Safety net: if migrations/bootstrapping have not seeded these rows yet,
        # create them before the dropdown is rendered.
        for role_name in STAFF_ROLE_NAMES:
            Role.objects.get_or_create(name=role_name)
        for status_name in DEFAULT_EMPLOYMENT_STATUS_NAMES:
            EmploymentStatus.objects.get_or_create(name=status_name)

        role_order = Case(*[When(name=name, then=Value(index)) for index, name in enumerate(STAFF_ROLE_NAMES)], output_field=IntegerField())
        self.fields['role'].queryset = Role.objects.filter(name__in=STAFF_ROLE_NAMES).annotate(role_order=role_order).order_by('role_order', 'name')
        self.fields['role'].empty_label = 'Select staff role'
        self.fields['subject'].empty_label = 'Select subject if applicable'
        self.fields['employment_status'].empty_label = 'Select employment status'
