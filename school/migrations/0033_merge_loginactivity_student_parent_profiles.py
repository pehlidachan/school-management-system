# Generated manually to merge Phase 1.5 student/parent profile migration with Phase 2.0 login audit migration.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("school", "0032_loginactivity"),
        ("school", "0032_student_parent_login_profiles"),
    ]

    operations = []
