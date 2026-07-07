from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .models import (
    AttendanceSession, ClassAndTiming, ClassIncharge, EmploymentStatus, Gender, Grade,
    GuardianRelation, LoginActivity, ParentProfile, Role, Staff, Student, StudentAttendance,
    StudentUserProfile, Subject,
)
from .finance_models import ExpenseCategory, FeeInvoice, SchoolExpense
from .notice_models import Notice
from .calendar_models import SchoolCalendarEvent
from .library_models import LibraryBook, LibraryIssue
from .message_models import MessageThread, ThreadMessage
from .exam_models import Exam, ExamSubject, StudentMark
from .gatepass_models import GatePass
from .non_teaching_models import NonTeachingStaff
from .public_models import JobApplication, OnlineAdmissionApplication, ParentComplaint


def safe_register(model, model_admin=None):
    try:
        admin.site.register(model, model_admin)
    except AlreadyRegistered:
        pass


class NameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'gr_no', 'admission_no', 'roll_no', 'grade',
        'father_name', 'guardian_name', 'whatsapp_no', 'monthly_fee',
        'welcome_card_sent', 'status',
    )
    list_filter = ('grade', 'status', 'gender', 'welcome_card_sent', 'rejoining_date')
    search_fields = (
        'name', 'student_name_urdu', 'father_name', 'guardian_name',
        'guardian_cnic', 'phone', 'whatsapp_no', 'email', 'gr_no',
        'admission_no', 'roll_no',
    )
    readonly_fields = ('photo_path', 'welcome_card_sent_at')


class StaffAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'staff_code', 'role', 'subject', 'department',
        'phone', 'whatsapp_no', 'employment_status', 'rejoining_date',
        'can_print_student_biodata', 'can_print_staff_biodata', 'status',
    )
    list_filter = (
        'role', 'subject', 'employment_status', 'status', 'department',
        'can_print_student_biodata', 'can_print_staff_biodata', 'birthday_card_sent',
    )
    search_fields = (
        'name', 'staff_name_urdu', 'staff_code', 'father_or_husband_name',
        'cnic', 'phone', 'whatsapp_no', 'email', 'qualification', 'department',
    )
    readonly_fields = ('photo_path',)


class ClassAndTimingAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_name', 'status')
    list_filter = ('status',)
    search_fields = ('class_name__name',)


class ClassInchargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'class_obj')
    search_fields = ('teacher__name', 'class_obj__class_name__name')


class StudentUserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'user', 'created_by', 'created_at')
    search_fields = ('student__name', 'user__username')


class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'guardian_name', 'student', 'user', 'created_by', 'created_at')
    search_fields = ('guardian_name', 'student__name', 'user__username')


class LoginActivityAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'username_entered', 'user', 'ip_address', 'is_successful', 'failure_reason', 'role_snapshot')
    list_filter = ('is_successful', 'created_at', 'country_code', 'city')
    search_fields = ('username_entered', 'user__username', 'ip_address', 'forwarded_for', 'user_agent', 'role_snapshot')
    readonly_fields = [field.name for field in LoginActivity._meta.fields]
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('attendance_date', 'grade', 'taken_by', 'created_at')
    list_filter = ('grade', 'attendance_date')
    search_fields = ('grade__name', 'taken_by__username', 'note')


class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('session', 'student', 'status', 'marked_by', 'updated_at')
    list_filter = ('status', 'session__grade', 'session__attendance_date')
    search_fields = ('student__name', 'remarks')


class FeeInvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'title', 'billing_month', 'due_date', 'amount_paid', 'status')
    list_filter = ('status', 'due_date', 'student__grade')
    search_fields = ('student__name', 'title', 'billing_month', 'payment_method')


class SchoolExpenseAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'category', 'title', 'amount', 'paid_to', 'payment_method')
    list_filter = ('category', 'payment_date')
    search_fields = ('title', 'paid_to', 'payment_method', 'note')


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('publish_date', 'title', 'audience', 'priority', 'is_published', 'view_count')
    list_filter = ('audience', 'priority', 'is_published', 'publish_date')
    search_fields = ('title', 'body')


class SchoolCalendarEventAdmin(admin.ModelAdmin):
    list_display = ('event_date', 'title', 'event_type', 'audience', 'location', 'is_active')
    list_filter = ('event_type', 'audience', 'is_active', 'event_date')
    search_fields = ('title', 'description', 'location')


class LibraryBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'accession_number', 'category', 'total_copies', 'available_copies', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'author', 'isbn', 'accession_number', 'publisher')


class LibraryIssueAdmin(admin.ModelAdmin):
    list_display = ('book', 'student', 'issue_date', 'due_date', 'return_date', 'status')
    list_filter = ('status', 'issue_date', 'due_date')
    search_fields = ('book__title', 'book__accession_number', 'student__name', 'remarks')


class MessageThreadAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'priority', 'is_read', 'last_activity_at')
    list_filter = ('priority', 'is_read', 'last_activity_at')
    search_fields = ('subject', 'sender__username', 'recipient__username')


class ThreadMessageAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at')
    search_fields = ('thread__subject', 'author__username', 'body')


class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'start_date', 'end_date', 'is_published')
    list_filter = ('grade', 'is_published', 'start_date')
    search_fields = ('name', 'grade__name')


class ExamSubjectAdmin(admin.ModelAdmin):
    list_display = ('exam', 'subject', 'total_marks', 'passing_marks')
    list_filter = ('exam__grade', 'subject')
    search_fields = ('exam__name', 'subject__name')


class StudentMarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam_subject', 'marks_obtained', 'marked_by', 'updated_at')
    list_filter = ('exam_subject__exam', 'exam_subject__subject')
    search_fields = ('student__name', 'exam_subject__exam__name', 'exam_subject__subject__name')


class GatePassAdmin(admin.ModelAdmin):
    list_display = ('id', 'person_type', 'person_name', 'student', 'staff', 'phone', 'status', 'created_at')
    list_filter = ('person_type', 'status', 'created_at')
    search_fields = ('person_name', 'phone', 'reason', 'destination', 'student__name', 'staff__name')


class NonTeachingStaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'appointment', 'department', 'phone', 'employment_status', 'status', 'joining_date')
    list_filter = ('status', 'department', 'employment_status', 'joining_date')
    search_fields = ('name', 'appointment', 'work_detail', 'phone', 'email', 'department')


class ParentComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_name', 'student_name', 'phone', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('parent_name', 'student_name', 'phone', 'subject', 'message', 'admin_note')


class OnlineAdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_name', 'father_name', 'desired_class', 'guardian_phone', 'status', 'created_at')
    list_filter = ('status', 'desired_class', 'created_at')
    search_fields = ('student_name', 'father_name', 'guardian_phone', 'previous_school', 'note')


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant_name', 'applied_for', 'phone', 'status', 'created_at')
    list_filter = ('status', 'applied_for', 'created_at')
    search_fields = ('applicant_name', 'applied_for', 'phone', 'qualification', 'experience', 'cover_note')


safe_register(Gender, NameAdmin)
safe_register(Grade, NameAdmin)
safe_register(GuardianRelation, NameAdmin)
safe_register(Role, NameAdmin)
safe_register(Subject, NameAdmin)
safe_register(EmploymentStatus, NameAdmin)
safe_register(Student, StudentAdmin)
safe_register(Staff, StaffAdmin)
safe_register(ClassAndTiming, ClassAndTimingAdmin)
safe_register(ClassIncharge, ClassInchargeAdmin)
safe_register(StudentUserProfile, StudentUserProfileAdmin)
safe_register(ParentProfile, ParentProfileAdmin)
safe_register(LoginActivity, LoginActivityAdmin)
safe_register(AttendanceSession, AttendanceSessionAdmin)
safe_register(StudentAttendance, StudentAttendanceAdmin)
safe_register(FeeInvoice, FeeInvoiceAdmin)
safe_register(ExpenseCategory, NameAdmin)
safe_register(SchoolExpense, SchoolExpenseAdmin)
safe_register(Notice, NoticeAdmin)
safe_register(SchoolCalendarEvent, SchoolCalendarEventAdmin)
safe_register(LibraryBook, LibraryBookAdmin)
safe_register(LibraryIssue, LibraryIssueAdmin)
safe_register(MessageThread, MessageThreadAdmin)
safe_register(ThreadMessage, ThreadMessageAdmin)
safe_register(Exam, ExamAdmin)
safe_register(ExamSubject, ExamSubjectAdmin)
safe_register(StudentMark, StudentMarkAdmin)
safe_register(GatePass, GatePassAdmin)
safe_register(NonTeachingStaff, NonTeachingStaffAdmin)
safe_register(ParentComplaint, ParentComplaintAdmin)
safe_register(OnlineAdmissionApplication, OnlineAdmissionApplicationAdmin)
safe_register(JobApplication, JobApplicationAdmin)

from . import admin_mvp  # noqa: F401, E402
