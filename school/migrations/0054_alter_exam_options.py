# Generated to keep the committed migration state aligned with the current Exam Meta ordering.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0053_academic_class_scheme'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exam',
            options={'ordering': ['academic_year', 'grade__name', 'sequence', 'start_date', 'name']},
        ),
    ]
