from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .exam_models import Exam, ExamDateSheetItem, ExamScheme, ExamSchemeItem, ExamSubject, StudentMark
from .ledger_models import CashBankAccount, CashBankTransaction, Vendor, VendorLedgerEntry
from .profile_settings_models import RoleProfileRule, SchoolBrandProfile, StaffLoginProfile, UserProfileSetting
from .staff_attendance_models import StaffLectureAttendance, StaffLectureSession
from .study_material_models import StudyMaterial


def safe_mvp_register(model, model_admin=None):
    try:
        admin.site.register(model, model_admin)
    except AlreadyRegistered:
        pass


class StaffLectureSessionAdmin(admin.ModelAdmin):
    list_display = ('session_date', 'title', 'taken_by', 'created_at')
    list_filter = ('session_date', 'taken_by')
    search_fields = ('title', 'note', 'taken_by__username')
    date_hierarchy = 'session_date'


class StaffLectureAttendanceAdmin(admin.ModelAdmin):
    list_display = ('session', 'staff', 'status', 'lecture_title', 'marked_by', 'updated_at')
    list_filter = ('status', 'session__session_date', 'staff__role', 'staff__subject')
    search_fields = ('staff__name', 'staff__staff_code', 'lecture_title', 'remarks')


class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'grade', 'subject', 'is_published', 'created_by', 'created_at')
    list_filter = ('grade', 'subject', 'is_published', 'created_at')
    search_fields = ('title', 'description', 'content', 'external_url')


class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'address', 'note')


class VendorLedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('entry_date', 'vendor', 'description', 'debit', 'credit', 'payment_method', 'created_by')
    list_filter = ('entry_date', 'vendor', 'payment_method')
    search_fields = ('vendor__name', 'description', 'note', 'payment_method')
    date_hierarchy = 'entry_date'


class CashBankAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_type', 'opening_balance', 'status', 'created_at')
    list_filter = ('account_type', 'status')
    search_fields = ('name',)


class CashBankTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_date', 'account', 'title', 'transaction_type', 'amount', 'created_by')
    list_filter = ('transaction_type', 'transaction_date', 'account')
    search_fields = ('account__name', 'title', 'note')
    date_hierarchy = 'transaction_date'


class SchoolBrandProfileAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'campus_code', 'phone', 'is_active', 'updated_by', 'updated_at')
    list_filter = ('is_active', 'updated_at')
    search_fields = ('school_name', 'campus_code', 'address', 'phone', 'email')


class UserProfileSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'phone', 'updated_at')
    search_fields = ('user__username', 'display_name', 'phone', 'note')


class StaffLoginProfileAdmin(admin.ModelAdmin):
    list_display = ('staff', 'user', 'created_by', 'created_at')
    search_fields = ('staff__name', 'staff__staff_code', 'user__username')
    list_filter = ('created_at',)


class RoleProfileRuleAdmin(admin.ModelAdmin):
    list_display = ('role', 'can_manage_branding', 'can_upload_self_photo', 'can_create_staff_accounts', 'can_change_own_password', 'can_manage_role_rules', 'dashboard_scope')
    list_filter = ('can_manage_branding', 'can_create_staff_accounts', 'can_manage_role_rules')
    search_fields = ('role__name', 'dashboard_scope', 'note')


class ExamSchemeItemInline(admin.TabularInline):
    model = ExamSchemeItem
    extra = 1
    fields = ('item_key', 'display_name', 'sequence', 'result_weight', 'default_total_marks', 'default_passing_marks', 'include_in_final_result', 'is_major_exam', 'is_active')


class ExamSchemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'school_brand', 'is_default', 'is_active', 'created_by', 'updated_at')
    list_filter = ('is_default', 'is_active', 'school_brand')
    search_fields = ('name', 'code', 'description', 'school_brand__school_name')
    inlines = [ExamSchemeItemInline]


class ExamSchemeItemAdmin(admin.ModelAdmin):
    list_display = ('scheme', 'display_name', 'item_key', 'sequence', 'result_weight', 'default_total_marks', 'default_passing_marks', 'include_in_final_result', 'is_major_exam', 'is_active')
    list_filter = ('scheme', 'include_in_final_result', 'is_major_exam', 'is_active')
    search_fields = ('scheme__name', 'item_key', 'display_name', 'note')


class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'scheme', 'scheme_item', 'exam_type', 'academic_year', 'grade', 'sequence', 'result_weight', 'is_locked', 'is_published', 'start_date')
    list_filter = ('scheme', 'exam_type', 'academic_year', 'grade', 'is_locked', 'is_published')
    search_fields = ('name', 'term_label', 'grade__name', 'scheme__name', 'scheme_item__display_name')
    date_hierarchy = 'start_date'


class ExamSubjectAdmin(admin.ModelAdmin):
    list_display = ('exam', 'subject', 'total_marks', 'passing_marks')
    list_filter = ('exam__scheme', 'exam__exam_type', 'exam__academic_year', 'exam__grade')
    search_fields = ('exam__name', 'subject__name')


class ExamDateSheetItemAdmin(admin.ModelAdmin):
    list_display = ('exam_subject', 'paper_date', 'start_time', 'end_time', 'room', 'sort_order')
    list_filter = ('paper_date', 'exam_subject__exam__scheme', 'exam_subject__exam__exam_type', 'exam_subject__exam__grade')
    search_fields = ('exam_subject__exam__name', 'exam_subject__subject__name', 'room', 'instructions')
    date_hierarchy = 'paper_date'


class StudentMarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam_subject', 'marks_obtained', 'marked_by', 'updated_at')
    list_filter = ('exam_subject__exam__scheme', 'exam_subject__exam__exam_type', 'exam_subject__exam__academic_year', 'exam_subject__exam__grade')
    search_fields = ('student__name', 'student__gr_no', 'exam_subject__exam__name', 'exam_subject__subject__name')


safe_mvp_register(StaffLectureSession, StaffLectureSessionAdmin)
safe_mvp_register(StaffLectureAttendance, StaffLectureAttendanceAdmin)
safe_mvp_register(StudyMaterial, StudyMaterialAdmin)
safe_mvp_register(Vendor, VendorAdmin)
safe_mvp_register(VendorLedgerEntry, VendorLedgerEntryAdmin)
safe_mvp_register(CashBankAccount, CashBankAccountAdmin)
safe_mvp_register(CashBankTransaction, CashBankTransactionAdmin)
safe_mvp_register(SchoolBrandProfile, SchoolBrandProfileAdmin)
safe_mvp_register(UserProfileSetting, UserProfileSettingAdmin)
safe_mvp_register(StaffLoginProfile, StaffLoginProfileAdmin)
safe_mvp_register(RoleProfileRule, RoleProfileRuleAdmin)
safe_mvp_register(ExamScheme, ExamSchemeAdmin)
safe_mvp_register(ExamSchemeItem, ExamSchemeItemAdmin)
safe_mvp_register(Exam, ExamAdmin)
safe_mvp_register(ExamSubject, ExamSubjectAdmin)
safe_mvp_register(ExamDateSheetItem, ExamDateSheetItemAdmin)
safe_mvp_register(StudentMark, StudentMarkAdmin)
