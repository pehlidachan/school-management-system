# Generated for TTM-CLASS-PERIOD-01 weekly timetable teacher mapping.

from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0054_alter_exam_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyTimetableSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.PositiveSmallIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], default=1)),
                ('period_number', models.PositiveSmallIntegerField(default=1, help_text='Period number in the selected day. Example: 1 to 7.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('room', models.CharField(blank=True, max_length=80)),
                ('is_break', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekly_timetable_slots', to='school.academicclass')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_weekly_timetable_slots', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weekly_timetable_slots', to='school.subject')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weekly_timetable_slots', to='school.staff')),
            ],
            options={
                'app_label': 'school',
                'ordering': ['academic_class__level_order', 'academic_class__class_label', 'day_of_week', 'period_number', 'start_time'],
                'indexes': [
                    models.Index(fields=['academic_class', 'day_of_week', 'period_number'], name='tt_slot_class_day_period_idx'),
                    models.Index(fields=['teacher', 'day_of_week', 'start_time'], name='tt_slot_teacher_day_time_idx'),
                    models.Index(fields=['subject', 'day_of_week'], name='tt_slot_subject_day_idx'),
                    models.Index(fields=['status', 'day_of_week'], name='tt_slot_status_day_idx'),
                ],
                'constraints': [
                    models.UniqueConstraint(fields=('academic_class', 'day_of_week', 'period_number'), name='unique_class_day_period_slot'),
                    models.UniqueConstraint(condition=models.Q(('is_break', False), ('status', True), ('teacher__isnull', False)), fields=('teacher', 'day_of_week', 'period_number'), name='unique_teacher_day_period_slot'),
                ],
            },
        ),
    ]
