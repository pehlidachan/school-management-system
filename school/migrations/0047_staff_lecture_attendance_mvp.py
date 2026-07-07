# Generated for staff lecture attendance MVP on 2026-07-07

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0046_student_monthly_fee_validator'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffLectureSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_date', models.DateField(default=django.utils.timezone.localdate)),
                ('title', models.CharField(default='Daily Staff Lecture Attendance', max_length=160)),
                ('note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('taken_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='taken_staff_lecture_sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-session_date', '-created_at'],
                'indexes': [models.Index(fields=['session_date'], name='school_staf_session_c7b9d1_idx')],
            },
        ),
        migrations.CreateModel(
            name='StaffLectureAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late'), ('leave', 'Leave')], default='present', max_length=20)),
                ('lecture_title', models.CharField(blank=True, max_length=160)),
                ('remarks', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('marked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marked_staff_lecture_attendance', to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='school.stafflecturesession')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecture_attendance_records', to='school.staff')),
            ],
            options={
                'ordering': ['staff__name'],
                'indexes': [models.Index(fields=['status'], name='school_staf_status_c25966_idx'), models.Index(fields=['staff', 'status'], name='school_staf_staff_i_5d46f4_idx')],
                'constraints': [models.UniqueConstraint(fields=('session', 'staff'), name='unique_staff_lecture_attendance')],
            },
        ),
    ]
