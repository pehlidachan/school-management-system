from django.conf import settings
from django.db import models


class Grade(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


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
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    welcome_card_sent = models.BooleanField(default=False)
    welcome_card_sent_at = models.DateTimeField(null=True, blank=True)
    photo_path = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)


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

    def __str__(self):
        return f'{self.id}---{self.name}'


class ClassAndTiming(models.Model):
    class_name = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
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

    def __str__(self):
        return f'{self.id}---{self.class_name}'


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
