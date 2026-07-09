import django.core.validators
import django.db.models.deletion
from django.db import migrations, models
from django.utils import timezone
from django.utils.text import slugify


def seed_academic_classes(apps, schema_editor):
    Grade = apps.get_model('school', 'Grade')
    AcademicSession = apps.get_model('school', 'AcademicSession')
    AcademicClass = apps.get_model('school', 'AcademicClass')
    ClassAndTiming = apps.get_model('school', 'ClassAndTiming')
    Student = apps.get_model('school', 'Student')

    session, _ = AcademicSession.objects.get_or_create(
        code='session-2026',
        defaults={
            'name': 'Session 2026',
            'start_date': timezone.localdate(),
            'is_active': True,
            'is_admission_open': True,
        },
    )

    class_map = {}
    for index, grade in enumerate(Grade.objects.all().order_by('name'), start=1):
        class_code = f"default-session-2026-{slugify(grade.name)}-a"[:120]
        academic_class, _ = AcademicClass.objects.get_or_create(
            class_code=class_code,
            defaults={
                'academic_session': session,
                'grade': grade,
                'section': 'A',
                'class_label': f"{grade.name} - A",
                'level_order': index,
                'capacity': 40,
                'admission_open': True,
                'monthly_fee': 0,
                'status': getattr(grade, 'status', True),
            },
        )
        class_map[grade.id] = academic_class

    for item in ClassAndTiming.objects.select_related('class_name').all():
        if item.class_name_id and item.class_name_id in class_map and not item.academic_class_id:
            item.academic_class = class_map[item.class_name_id]
            item.save(update_fields=['academic_class'])

    for student in Student.objects.all():
        if student.grade_id and student.grade_id in class_map and not student.academic_class_id:
            student.academic_class = class_map[student.grade_id]
            student.save(update_fields=['academic_class'])


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0052_exam_scheme_templates'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Session 2026', max_length=120)),
                ('code', models.SlugField(default='session-2026', max_length=80, unique=True)),
                ('start_date', models.DateField(default=timezone.localdate)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admission_open', models.BooleanField(default=True)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('school_brand', models.ForeignKey(blank=True, help_text='Optional school/campus attachment for future SaaS mode.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='academic_sessions', to='school.schoolbrandprofile')),
            ],
            options={
                'ordering': ['-is_active', '-start_date', 'name'],
                'indexes': [models.Index(fields=['code'], name='academic_session_code_idx'), models.Index(fields=['is_active'], name='academic_session_active_idx'), models.Index(fields=['school_brand'], name='academic_session_school_idx')],
            },
        ),
        migrations.CreateModel(
            name='AcademicClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(default='A', max_length=20)),
                ('class_label', models.CharField(blank=True, max_length=140)),
                ('class_code', models.SlugField(blank=True, max_length=120, unique=True)),
                ('level_order', models.PositiveSmallIntegerField(default=1)),
                ('room', models.CharField(blank=True, max_length=80)),
                ('capacity', models.PositiveSmallIntegerField(default=40)),
                ('admission_open', models.BooleanField(default=True)),
                ('monthly_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.BooleanField(default=True)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='school.academicsession')),
                ('class_teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_academic_classes', to='school.staff')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academic_classes', to='school.grade')),
                ('promotion_target', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promotion_sources', to='school.academicclass')),
                ('school_brand', models.ForeignKey(blank=True, help_text='Optional school/campus attachment for future SaaS mode.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='academic_classes', to='school.schoolbrandprofile')),
            ],
            options={
                'ordering': ['academic_session__name', 'level_order', 'grade__name', 'section'],
                'indexes': [models.Index(fields=['school_brand', 'academic_session'], name='acad_class_school_session_idx'), models.Index(fields=['academic_session', 'grade', 'section'], name='acad_class_session_grade_idx'), models.Index(fields=['class_code'], name='academic_class_code_idx'), models.Index(fields=['status'], name='academic_class_status_idx'), models.Index(fields=['admission_open'], name='academic_class_adm_idx')],
                'constraints': [models.UniqueConstraint(fields=('academic_session', 'grade', 'section', 'school_brand'), name='unique_academic_class_per_session')],
            },
        ),
        migrations.CreateModel(
            name='AcademicClassSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_core', models.BooleanField(default=True)),
                ('weekly_periods', models.PositiveSmallIntegerField(default=5)),
                ('total_marks', models.DecimalField(decimal_places=2, default=100, max_digits=7)),
                ('passing_marks', models.DecimalField(decimal_places=2, default=33, max_digits=7)),
                ('sort_order', models.PositiveSmallIntegerField(default=1)),
                ('status', models.BooleanField(default=True)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('academic_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_scheme', to='school.academicclass')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academic_class_subjects', to='school.subject')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='academic_subject_assignments', to='school.staff')),
            ],
            options={
                'ordering': ['academic_class', 'sort_order', 'subject__name'],
                'indexes': [models.Index(fields=['academic_class', 'sort_order'], name='acad_class_subject_order_idx'), models.Index(fields=['teacher'], name='acad_class_subject_teacher_idx'), models.Index(fields=['status'], name='acad_class_subject_status_idx')],
                'constraints': [models.UniqueConstraint(fields=('academic_class', 'subject'), name='unique_subject_per_academic_class')],
            },
        ),
        migrations.AddField(
            model_name='student',
            name='academic_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='school.academicclass'),
        ),
        migrations.AddField(
            model_name='classandtiming',
            name='academic_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='timetables', to='school.academicclass'),
        ),
        migrations.RunPython(seed_academic_classes, migrations.RunPython.noop),
    ]
