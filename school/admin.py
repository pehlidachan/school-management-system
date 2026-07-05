from django.contrib import admin
from .models import Gender, Grade, GuardianRelation, Student, Role, Subject, EmploymentStatus, Staff, ClassAndTiming, ClassIncharge, StudentUserProfile, ParentProfile, LoginActivity
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


admin.site.register(StudentUserProfile, StudentUserProfileAdmin)
admin.site.register(ParentProfile, ParentProfileAdmin)
admin.site.register(LoginActivity, LoginActivityAdmin)
