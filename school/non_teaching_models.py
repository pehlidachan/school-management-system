from django.db import models

from .models import EmploymentStatus, Gender


class NonTeachingStaff(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.CharField(max_length=255)
    work_detail = models.TextField(blank=True)
    department = models.CharField(max_length=255, blank=True)
    qualification = models.CharField(max_length=255, blank=True)
    experience = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=500, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    salary = models.CharField(max_length=50, blank=True)
    employment_status = models.ForeignKey(EmploymentStatus, on_delete=models.SET_NULL, null=True, blank=True)
    contract_details = models.TextField(blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'school'
        ordering = ['name']

    def __str__(self):
        return f'{self.id} - {self.name} ({self.appointment})'
