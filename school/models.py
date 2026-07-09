from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Grade(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AcademicSession(models.Model):
    name = models.CharField(max_length=120, default="Session 2026")
    code = models.SlugField(max_length=80, unique=True, default="session-2026")
    school_brand = models.ForeignKey(
        "school.SchoolBrandProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="academic_sessions",
        help_text="Optional school/campus attachment for future SaaS mode.",
    )
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admission_open = models.BooleanField(default=True)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["-is_active", "-start_date", "name"]
        indexes = [
            models.Index(fields=["code"], name="academic_session_code_idx"),
            models.Index(fields=["is_active"], name="academic_session_active_idx"),
            models.Index(fields=["school_brand"], name="academic_session_school_idx"),
        ]

    def __str__(self):
        return self.name


class AcademicClass(models.Model):
    school_brand = models.ForeignKey(
        "school.SchoolBrandProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="academic_classes",
        help_text="Optional school/campus attachment for future SaaS mode.",
    )
    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name="classes",
    )
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="academic_classes")
    section = models.CharField(max_length=20, default="A")
    class_label = models.CharField(max_length=140, blank=True)
    class_code = models.SlugField(max_length=120, unique=True, blank=True)
    level_order = models.PositiveSmallIntegerField(default=1)
    room = models.CharField(max_length=80, blank=True)
    capacity = models.PositiveSmallIntegerField(default=40)
    class_teacher = models.ForeignKey(
        "school.Staff",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_academic_classes",
    )
    admission_open = models.BooleanField(default=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    promotion_target = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="promotion_sources",
    )
    status = models.BooleanField(default=True)
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "school"
        ordering = ["academic_session__name", "level_order", "grade__name", "section"]
        indexes = [
            models.Index(fields=["school_brand", "academic_session"], name="acad_class_school_session_idx"),
            models.Index(fields=["academic_session", "grade", "section"], name="acad_class_session_grade_idx"),
            models.Index(fields=["class_code"], name="academic_class_code_idx"),
            models.Index(fields=["status"], name="academic_class_status_idx"),
            models.Index(fields=["admission_open"], name="academic_class_adm_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["academic_session", "grade", "section", "school_brand"],
                name="unique_academic_class_per_session",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.class_label:
            self.class_label = f"{self.grade} - {self.section}"
        if not self.class_code:
            brand_key = "default"
            if self.school_brand_id and self.school_brand:
                brand_key = self.school_brand.campus_code or self.school_brand.school_name or "school"
            session_key = self.academic_session.code if self.academic_session_id and self.academic_session else "session"
            self.class_code = slugify(f"{brand_key}-{session_key}-{self.grade}-{self.section}")[:120]
        super().save(*args, **kwargs)

    @property
    def enrolled_students_count(self):
        return self.students.filter(status=True).count()

    @property
    def seats_available(self):
        return max(int(self.capacity or 0) - int(self.enrolled_students_count or 0), 0)

    def __str__(self):
        return self.class_label or f"{self.grade} - {self.section}"


class Gender(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class GuardianRelation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=255)
    gr_no = models.CharField(max_length=50, null=True, blank=True)
    admission_no = models.CharField(max_length=50, null=True, blank=True)
    roll_no = models.CharField(max_length=50, null=True, blank=True)
    student_name_urdu = models.CharField(max_length=150, null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    academic_class = models.ForeignKey(
        AcademicClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    age = models.IntegerField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    dob = models.DateField()
    guardian_name = models.CharField(max_length=255)
    guardian_relation = models.ForeignKey(GuardianRelation, on_delete=models.CASCADE)
    guardian_cnic = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=500)
    date_of_enrollment = models.DateField()
    rejoining_date = models.DateField(null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    mother_mobile = models.CharField(max_length=100, null=True, blank=True)
    whatsapp_no = models.CharField(max_length=100, null=True, blank=True)
    emergency_phone = models.CharField(max_length=100)
    previous_school = models.CharField(max_length=200, null=True, blank=True)
    blood_group = models.CharField(max_length=20, null=True, blank=True)
    fee_category = models.CharField(max_length=100, null=True, blank=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    welcome_card_sent = models.BooleanField(default=False)
    welcome_card_sent_at = models.DateTimeField(null=True, blank=True)
    photo_path = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    def clean(self):
        super().clean()
        errors = {}
        for field_name, label in (("gr_no", "GR number"), ("admission_no", "admission number")):
            value = (getattr(self, field_name) or "").strip()
            if not value:
                continue
            setattr(self, field_name, value)
            duplicates = Student.objects.filter(**{f"{field_name}__iexact": value})
            if self.pk:
                duplicates = duplicates.exclude(pk=self.pk)
            if duplicates.exists():
                errors[field_name] = f"This {label} is already used by another student."
        if self.academic_class_id and self.grade_id and self.academic_class.grade_id != self.grade_id:
            errors["academic_class"] = "Academic class must belong to the selected grade."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.academic_class_id and self.academic_class and self.grade_id != self.academic_class.grade_id:
            self.grade = self.academic_class.grade
        if self.welcome_card_sent:
            if not self.welcome_card_sent_at:
                self.welcome_card_sent_at = timezone.now()
        else:
            self.welcome_card_sent_at = None

        update_fields = kwargs.get("update_fields")
        if update_fields is not None and "welcome_card_sent" in update_fields:
            kwargs["update_fields"] = set(update_fields) | {"welcome_card_sent_at"}

        super().save(*args, **kwargs)


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class EmploymentStatus(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=255)
    staff_code = models.CharField(max_length=50, null=True, blank=True)
    staff_name_urdu = models.CharField(max_length=150, null=True, blank=True)
    father_or_husband_name = models.CharField(max_length=255, null=True, blank=True)
    cnic = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField()
    dob = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=255)
    experience = models.CharField(max_length=255, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    whatsapp_no = models.CharField(max_length=100, null=True, blank=True)
    emergency_phone = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    department = models.CharField(max_length=100, null=True, blank=True)
    joining_date = models.DateField()
    rejoining_date = models.DateField(null=True, blank=True)
    salary = models.CharField(max_length=20)
    employment_status = models.ForeignKey(EmploymentStatus, on_delete=models.CASCADE)
    contract_details = models.CharField(max_length=1000, null=True, blank=True)
    can_print_student_biodata = models.BooleanField(default=False)
    can_print_staff_biodata = models.BooleanField(default=False)
    birthday_card_sent = models.BooleanField(default=False)
    photo_path = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    def clean(self):
        super().clean()
        errors = {}
        for field_name, label in (("staff_code", "staff code"), ("cnic", "CNIC")):
            value = (getattr(self, field_name) or "").strip()
            if not value:
                continue
            setattr(self, field_name, value)
            duplicates = Staff.objects.filter(**{f"{field_name}__iexact": value})
            if self.pk:
                duplicates = duplicates.exclude(pk=self.pk)
            if duplicates.exists():
                errors[field_name] = f"This {label} is already used by another staff member."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{self.id}---{self.name}'


class AcademicClassSubject(models.Model):
    academic_class = models.ForeignKey(
        AcademicClass,
        on_delete=models.CASCADE,
        related_name="subject_scheme",
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="academic_class_subjects")
    teacher = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="academic_subject_assignments",
    )
    is_core = models.BooleanField(default=True)
    weekly_periods = models.PositiveSmallIntegerField(default=5)
    total_marks = models.DecimalField(max_digits=7, decimal_places=2, default=100)
    passing_marks = models.DecimalField(max_digits=7, decimal_places=2, default=33)
    sort_order = models.PositiveSmallIntegerField(default=1)
    status = models.BooleanField(default=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        app_label = "school"
        ordering = ["academic_class", "sort_order", "subject__name"]
        constraints = [
            models.UniqueConstraint(fields=["academic_class", "subject"], name="unique_subject_per_academic_class"),
        ]
        indexes = [
            models.Index(fields=["academic_class", "sort_order"], name="acad_class_subject_order_idx"),
            models.Index(fields=["teacher"], name="acad_class_subject_teacher_idx"),
            models.Index(fields=["status"], name="acad_class_subject_status_idx"),
        ]

    def __str__(self):
        return f"{self.academic_class} - {self.subject}"


class ClassAndTiming(models.Model):
    class_name = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    academic_class = models.ForeignKey(AcademicClass, on_delete=models.SET_NULL, null=True, blank=True, related_name="timetables")
    period_one_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_one_subject')
    period_one_teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_one_teacher')
    period_one_from = models.TimeField(default='00:00:00')
    period_one_to = models.TimeField(default='00:00:00')
    period_two_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_two_subject')
    period_two_teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_two_teacher')
    period_two_from = models.TimeField(default='00:00:00')
    period_two_to = models.TimeField(default='00:00:00')
    period_three_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_three_subject')
    period_three_teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_three_teacher')
    period_three_from = models.TimeField(default='00:00:00')
    period_three_to = models.TimeField(default='00:00:00')
    period_four_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_four_subject')
    period_four_teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_four_teacher')
    period_four_from = models.TimeField(default='00:00:00')
    period_four_to = models.TimeField(default='00:00:00')
    period_five_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_five_subject')
    period_five_teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_five_teacher')
    period_five_from = models.TimeField(default='00:00:00')
    period_five_to = models.TimeField(default='00:00:00')
    period_six_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_six_subject')
    period_six_teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_six_teacher')
    period_six_from = models.TimeField(default='00:00:00')
    period_six_to = models.TimeField(default='00:00:00')
    period_seven_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_seven_subject')
    period_seven_teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='period_seven_teacher')
    period_seven_from = models.TimeField(default='00:00:00')
    period_seven_to = models.TimeField(default='00:00:00')
    status = models.BooleanField(default=True)

    def clean(self):
        super().clean()
        if self.academic_class_id and self.class_name_id and self.academic_class.grade_id != self.class_name_id:
            raise ValidationError({"academic_class": "Academic class grade must match class name / grade."})

    def save(self, *args, **kwargs):
        if self.academic_class_id and self.academic_class:
            self.class_name = self.academic_class.grade
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}---{self.academic_class or self.class_name}'


class ClassIncharge(models.Model):
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(ClassAndTiming, on_delete=models.CASCADE)


class StudentUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='login_profile')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_student_login_profiles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Student login: {self.student.name} -> {self.user.username}'


class ParentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_profile')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parent_profiles')
    guardian_name = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_parent_login_profiles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Parent login: {self.guardian_name} -> {self.user.username}'


class LoginActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='login_activities')
    username_entered = models.CharField(max_length=150, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    forwarded_for = models.TextField(blank=True)
    user_agent = models.TextField(blank=True)
    path = models.CharField(max_length=255, blank=True)
    method = models.CharField(max_length=10, blank=True)
    is_successful = models.BooleanField(default=False)
    failure_reason = models.CharField(max_length=255, blank=True)
    session_key = models.CharField(max_length=100, blank=True)
    role_snapshot = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    region = models.CharField(max_length=120, blank=True)
    country_code = models.CharField(max_length=10, blank=True)
    country_name = models.CharField(max_length=120, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    timezone = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['is_successful']),
            models.Index(fields=['username_entered']),
        ]

    def __str__(self):
        return f'Login activity: {self.username_entered or self.user}'


class AttendanceSession(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='attendance_sessions')
    attendance_date = models.DateField()
    taken_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='taken_attendance_sessions')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-attendance_date', 'grade__name']
        constraints = [models.UniqueConstraint(fields=['grade', 'attendance_date'], name='unique_grade_attendance_date')]
        indexes = [
            models.Index(fields=['attendance_date']),
            models.Index(fields=['grade', 'attendance_date']),
        ]

    def __str__(self):
        return f'{self.grade} attendance on {self.attendance_date}'


class StudentAttendance(models.Model):
    PRESENT = 'present'
    ABSENT = 'absent'
    LATE = 'late'
    LEAVE = 'leave'
    STATUS_CHOICES = [(PRESENT, 'Present'), (ABSENT, 'Absent'), (LATE, 'Late'), (LEAVE, 'Leave')]
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PRESENT)
    remarks = models.CharField(max_length=255, blank=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='marked_student_attendance')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student__name']
        constraints = [models.UniqueConstraint(fields=['session', 'student'], name='unique_student_attendance_per_session')]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['student', 'status']),
        ]

    def __str__(self):
        return f'{self.student.name}: {self.status} ({self.session.attendance_date})'
