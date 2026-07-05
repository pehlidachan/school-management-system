from django.db import migrations

STAFF_ROLE_NAMES = [
    "Teacher",
    "Head of Department",
    "Principal",
    "Accountant",
]

DEFAULT_EMPLOYMENT_STATUS_NAMES = [
    "Permanent",
    "Contract",
    "Part Time",
    "Probation",
]


def seed_staff_roles_and_statuses(apps, schema_editor):
    Role = apps.get_model("school", "Role")
    EmploymentStatus = apps.get_model("school", "EmploymentStatus")

    for name in STAFF_ROLE_NAMES:
        Role.objects.get_or_create(name=name)

    for name in DEFAULT_EMPLOYMENT_STATUS_NAMES:
        EmploymentStatus.objects.get_or_create(name=name)


def noop_reverse(apps, schema_editor):
    # Keep seeded rows during rollback to avoid deleting user-used roles.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("school", "0030_initial"),
    ]

    operations = [
        migrations.RunPython(seed_staff_roles_and_statuses, noop_reverse),
    ]
