from django.db import models

from .models import Staff, Student
from .non_teaching_models import NonTeachingStaff


class StudentPortrait(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='portrait_record')
    image = models.FileField(upload_to='portraits/students/')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'school'

    def __str__(self):
        return f'Student portrait: {self.student.name}'


class StaffPortrait(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='portrait_record')
    image = models.FileField(upload_to='portraits/staff/')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'school'

    def __str__(self):
        return f'Staff portrait: {self.staff.name}'


class SupportStaffPortrait(models.Model):
    staff = models.OneToOneField(NonTeachingStaff, on_delete=models.CASCADE, related_name='portrait_record')
    image = models.FileField(upload_to='portraits/support_staff/')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'school'

    def __str__(self):
        return f'Support staff portrait: {self.staff.name}'
