from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from school.constants import DEFAULT_EMPLOYMENT_STATUS_NAMES, STAFF_ROLE_NAMES
from school.models import (
    ClassAndTiming,
    ClassIncharge,
    EmploymentStatus,
    Gender,
    Grade,
    GuardianRelation,
    Role,
    Staff,
    Student,
    StudentUserProfile,
    ParentProfile,
    Subject,
)

ROLE_MATRIX = {
    "School Admin": "all",
    "Principal": {
        "view": [Student, Staff, Grade, Gender, GuardianRelation, Role, Subject, EmploymentStatus, ClassAndTiming, ClassIncharge, StudentUserProfile, ParentProfile],
        "add": [Student, Staff, Grade, Gender, GuardianRelation, Role, Subject, EmploymentStatus, ClassAndTiming, ClassIncharge, StudentUserProfile, ParentProfile],
        "change": [Student, Staff, Grade, Gender, GuardianRelation, Role, Subject, EmploymentStatus, ClassAndTiming, ClassIncharge, StudentUserProfile, ParentProfile],
        "delete": [],
    },
    "Head of Department": {
        "view": [Student, Staff, Grade, Subject, ClassAndTiming, ClassIncharge],
        "add": [],
        "change": [],
        "delete": [],
    },
    "Teacher": {
        "view": [Student, Grade, Subject, ClassAndTiming, ClassIncharge],
        "add": [],
        "change": [],
        "delete": [],
    },
    "Student": {
        "view": [Student, Grade, Subject, ClassAndTiming],
        "add": [],
        "change": [],
        "delete": [],
    },
    "Parent": {
        "view": [Student, Grade, Subject, ClassAndTiming],
        "add": [],
        "change": [],
        "delete": [],
    },
    "Accountant": {
        "view": [Student, Staff, Grade, StudentUserProfile, ParentProfile],
        "add": [StudentUserProfile, ParentProfile],
        "change": [StudentUserProfile, ParentProfile],
        "delete": [],
    },
}

ALL_MODELS = [Student, Staff, Grade, Gender, GuardianRelation, Role, Subject, EmploymentStatus, ClassAndTiming, ClassIncharge, StudentUserProfile, ParentProfile]


class Command(BaseCommand):
    help = "Create default school role groups and attach safe starting permissions."

    def handle(self, *args, **options):
        for group_name, rules in ROLE_MATRIX.items():
            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions.clear()

            if rules == "all":
                perms = Permission.objects.filter(content_type__app_label="school")
                group.permissions.set(perms)
            else:
                permissions = []
                for action, models in rules.items():
                    for model in models:
                        content_type = ContentType.objects.get_for_model(model)
                        codename = f"{action}_{model._meta.model_name}"
                        perm = Permission.objects.filter(content_type=content_type, codename=codename).first()
                        if perm:
                            permissions.append(perm)
                group.permissions.set(permissions)

            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} group: {group_name}"))

        for role_name in STAFF_ROLE_NAMES:
            role, created = Role.objects.get_or_create(name=role_name)
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Ready'} staff role row: {role_name}"))

        for status_name in DEFAULT_EMPLOYMENT_STATUS_NAMES:
            status, created = EmploymentStatus.objects.get_or_create(name=status_name)
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Ready'} employment status row: {status_name}"))

        self.stdout.write(self.style.SUCCESS("Default school auth groups + staff role dropdown rows are ready."))
