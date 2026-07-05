from django.db import models


class ParentComplaint(models.Model):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    STATUS_CHOICES = [
        (NEW, "New"),
        (IN_PROGRESS, "In Progress"),
        (RESOLVED, "Resolved"),
    ]

    parent_name = models.CharField(max_length=255)
    student_name = models.CharField(max_length=255)
    student_class = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "school"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Complaint: {self.parent_name} - {self.subject}"


class OnlineAdmissionApplication(models.Model):
    NEW = "new"
    REVIEWED = "reviewed"
    CONTACTED = "contacted"
    STATUS_CHOICES = [
        (NEW, "New"),
        (REVIEWED, "Reviewed"),
        (CONTACTED, "Contacted"),
    ]

    student_name = models.CharField(max_length=255)
    desired_class = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    father_name = models.CharField(max_length=255)
    guardian_phone = models.CharField(max_length=100)
    guardian_email = models.EmailField(blank=True)
    previous_school = models.CharField(max_length=255, blank=True)
    address = models.TextField()
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "school"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Admission: {self.student_name} for {self.desired_class}"


class JobApplication(models.Model):
    NEW = "new"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    STATUS_CHOICES = [
        (NEW, "New"),
        (SHORTLISTED, "Shortlisted"),
        (REJECTED, "Rejected"),
    ]

    applicant_name = models.CharField(max_length=255)
    applied_for = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    experience = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    cover_note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "school"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Job: {self.applicant_name} - {self.applied_for}"
