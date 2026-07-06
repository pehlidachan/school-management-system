from django.core.management.base import BaseCommand
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


class Command(BaseCommand):
    help = 'Checks important school app URL names and templates.'

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
        if errors:
            raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS('School URL/template check passed.'))
