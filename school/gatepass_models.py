from django.conf import settings
from django.db import models
from django.utils import timezone

from .models import Staff, Student


class GatePass(models.Model):
    PERSON_STUDENT = 'student'
    PERSON_STAFF = 'staff'
    PERSON_WORKER = 'worker'
    PERSON_OTHER = 'other'
    PERSON_CHOICES = [
        (PERSON_STUDENT, 'Student'),
        (PERSON_STAFF, 'Staff Member'),
        (PERSON_WORKER, 'Maintenance Worker'),
        (PERSON_OTHER, 'Other Visitor'),
    ]

    STATUS_ISSUED = 'issued'
    STATUS_RETURNED = 'returned'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_ISSUED, 'Issued'),
        (STATUS_RETURNED, 'Returned'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    person_type = models.CharField(max_length=20, choices=PERSON_CHOICES, default=PERSON_STUDENT)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='gate_passes')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='gate_passes')
    person_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    destination = models.CharField(max_length=255, blank=True)
    reason = models.TextField()
    luggage_detail = models.TextField(blank=True)
    expected_return_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ISSUED)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='issued_gate_passes')
    created_at = models.DateTimeField(default=timezone.now)
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'school'
        ordering = ['-created_at']

    @property
    def display_name(self):
        if self.person_type == self.PERSON_STUDENT and self.student:
            return self.student.name
        if self.person_type == self.PERSON_STAFF and self.staff:
            return self.staff.name
        return self.person_name or '-'

    @property
    def gate_pass_no(self):
        return f'GP-{self.created_at:%Y%m%d}-{self.id or 0:04d}'

    def __str__(self):
        return f'{self.gate_pass_no} - {self.display_name}'
