from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection
from django.template.loader import get_template
from django.urls import NoReverseMatch, reverse


URL_NAMES = [
    'dashboard', 'portal', 'display_students', 'add_student', 'display_staff', 'add_staff',
    'non_teaching_staff_list', 'add_non_teaching_staff', 'attendance_dashboard',
    'finance_dashboard', 'notice_board', 'calendar_dashboard', 'library_dashboard',
    'message_inbox', 'exam_dashboard', 'gatepass_dashboard', 'multi_child_guardians',
]

TEMPLATES = [
    'dashboard.html', 'admin_portal_online.html', 'student_filtered_list.html',
    'staff_filtered_list_v3.html', 'non_teaching_staff_list.html',
    'non_teaching_staff_form.html', 'attendance_dashboard.html', 'finance_dashboard.html',
    'notice_board.html', 'calendar_dashboard.html', 'library_dashboard.html',
    'message_inbox.html', 'exam_dashboard.html', 'gatepass_dashboard.html',
    'multi_child_guardians.html',
]

MODEL_LABELS = [
    'school.Student', 'school.Staff', 'school.AttendanceSession', 'school.StudentAttendance',
    'school.FeeInvoice', 'school.SchoolExpense', 'school.Notice', 'school.SchoolCalendarEvent',
    'school.LibraryBook', 'school.LibraryIssue', 'school.MessageThread', 'school.ThreadMessage',
    'school.Exam', 'school.StudentMark', 'school.GatePass', 'school.NonTeachingStaff',
]


class Command(BaseCommand):
    help = 'Checks important school app URL names, templates and database tables.'

    def handle(self, *args, **options):
        errors = []
        for name in URL_NAMES:
            try:
                reverse(name)
                self.stdout.write(self.style.SUCCESS('URL OK: ' + name))
            except NoReverseMatch as exc:
                errors.append('URL FAIL: ' + name + ' -> ' + str(exc))
                self.stdout.write(self.style.ERROR(errors[-1]))
        for template_name in TEMPLATES:
            try:
                get_template(template_name)
                self.stdout.write(self.style.SUCCESS('TEMPLATE OK: ' + template_name))
            except Exception as exc:
                errors.append('TEMPLATE FAIL: ' + template_name + ' -> ' + str(exc))
                self.stdout.write(self.style.ERROR(errors[-1]))
        existing_tables = set(connection.introspection.table_names())
        for label in MODEL_LABELS:
            try:
                app_label, model_name = label.split('.')
                model = apps.get_model(app_label, model_name)
                table_name = model._meta.db_table
                if table_name in existing_tables:
                    self.stdout.write(self.style.SUCCESS('TABLE OK: ' + table_name))
                else:
                    errors.append('TABLE FAIL: ' + table_name + ' missing')
                    self.stdout.write(self.style.ERROR(errors[-1]))
            except Exception as exc:
                errors.append('MODEL FAIL: ' + label + ' -> ' + str(exc))
                self.stdout.write(self.style.ERROR(errors[-1]))
        if errors:
            raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS('School URL/template/table check passed.'))
