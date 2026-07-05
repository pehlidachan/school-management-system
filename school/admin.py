from django.contrib import admin
from .models import Gender, Grade, GuardianRelation, Student, Role, Subject, EmploymentStatus, Staff, ClassAndTiming, ClassIncharge, StudentUserProfile, ParentProfile, LoginActivity, AttendanceSession, StudentAttendance
from .finance_models import FeeInvoice, ExpenseCategory, SchoolExpense
from .notice_models import Notice
from .calendar_models import SchoolCalendarEvent
# Register your models here.

'''
///////////////////////
//   Student     //
///////////////////////
'''
class GenderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class GuardianRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'grade', 'age', 'gender', 'dob','guardian_name', 'guardian_relation', 'date_of_enrollment', 'email', 'phone','emergency_phone' , 'previous_school', 'status')


admin.site.register(Gender, GenderAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(GuardianRelation, GuardianRelationAdmin)
admin.site.register(Student, StudentAdmin)
'''
///////////////////////
//   Staff     //
///////////////////////
'''

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class EmployStatusAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'dob', 'gender', 'qualification', 'experience', 'role', 'subject', 'email', 'phone', 'emergency_phone', 'address', 'joining_date', 'salary', 'employment_status', 'contract_details', 'status')

admin.site.register(Role, RoleAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(EmploymentStatus, EmployStatusAdmin)
admin.site.register(Staff, StaffAdmin)


'''
///////////////////////////
//   ClassAndTime     //
///////////////////////////
'''

class ClassAndTimingAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_name', 'period_one_subject', 'period_one_teacher', 'period_two_subject', 'period_two_subject', 'period_three_subject', 'period_three_teacher', 'period_four_subject', 'period_four_teacher', 'period_five_subject', 'period_five_teacher', 'period_six_subject', 'period_six_teacher', 'period_seven_subject', 'period_seven_teacher', 'status')


class ClassInchargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'class_obj')

admin.site.register(ClassAndTiming, ClassAndTimingAdmin)
admin.site.register(ClassIncharge, ClassInchargeAdmin)



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
    readonly_fields = (
        'user', 'username_entered', 'ip_address', 'forwarded_for', 'user_agent',
        'path', 'method', 'is_successful', 'failure_reason', 'session_key',
        'role_snapshot', 'city', 'region', 'country_code', 'country_name',
        'latitude', 'longitude', 'timezone', 'created_at'
    )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('attendance_date', 'grade', 'taken_by', 'created_at', 'updated_at')
    list_filter = ('grade', 'attendance_date')
    search_fields = ('grade__name', 'taken_by__username', 'note')
    date_hierarchy = 'attendance_date'
    ordering = ('-attendance_date',)


class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('session', 'student', 'status', 'marked_by', 'updated_at')
    list_filter = ('status', 'session__grade', 'session__attendance_date')
    search_fields = ('student__name', 'session__grade__name', 'remarks')
    ordering = ('-session__attendance_date', 'student__name')


class FeeInvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'title', 'billing_month', 'due_date', 'amount_paid', 'status', 'created_by')
    list_filter = ('status', 'due_date', 'student__grade')
    search_fields = ('student__name', 'title', 'billing_month', 'payment_method')
    date_hierarchy = 'due_date'
    ordering = ('-due_date',)


class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    search_fields = ('name',)


class SchoolExpenseAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'category', 'title', 'amount', 'paid_to', 'payment_method', 'created_by')
    list_filter = ('category', 'payment_date')
    search_fields = ('title', 'paid_to', 'payment_method', 'note')
    date_hierarchy = 'payment_date'
    ordering = ('-payment_date',)


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('publish_date', 'title', 'audience', 'priority', 'is_published', 'created_by', 'view_count')
    list_filter = ('audience', 'priority', 'is_published', 'publish_date')
    search_fields = ('title', 'body', 'created_by__username')
    date_hierarchy = 'publish_date'
    ordering = ('-publish_date', '-created_at')


class SchoolCalendarEventAdmin(admin.ModelAdmin):
    list_display = ('event_date', 'title', 'event_type', 'audience', 'location', 'is_active', 'created_by')
    list_filter = ('event_type', 'audience', 'is_active', 'event_date')
    search_fields = ('title', 'description', 'location', 'created_by__username')
    date_hierarchy = 'event_date'
    ordering = ('event_date', 'start_time')


admin.site.register(StudentUserProfile, StudentUserProfileAdmin)
admin.site.register(ParentProfile, ParentProfileAdmin)
admin.site.register(LoginActivity, LoginActivityAdmin)
admin.site.register(AttendanceSession, AttendanceSessionAdmin)
admin.site.register(StudentAttendance, StudentAttendanceAdmin)
admin.site.register(FeeInvoice, FeeInvoiceAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
admin.site.register(SchoolExpense, SchoolExpenseAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(SchoolCalendarEvent, SchoolCalendarEventAdmin)
