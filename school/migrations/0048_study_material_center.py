# Generated for study material center MVP on 2026-07-07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0047_staff_lecture_attendance_mvp'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180)),
                ('description', models.TextField(blank=True)),
                ('content', models.TextField(blank=True)),
                ('external_url', models.URLField(blank=True)),
                ('is_published', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_study_materials', to=settings.AUTH_USER_MODEL)),
                ('grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_materials', to='school.grade')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='study_materials', to='school.subject')),
            ],
            options={
                'ordering': ['-created_at', 'grade__name', 'subject__name'],
                'indexes': [models.Index(fields=['is_published'], name='school_stud_is_publ_0a8aa9_idx'), models.Index(fields=['grade', 'subject'], name='school_stud_grade_i_aad513_idx')],
            },
        ),
    ]
