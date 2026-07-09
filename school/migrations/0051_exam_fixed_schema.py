from decimal import Decimal

from django.db import migrations, models
import django.db.models.deletion


def set_exam_schema_defaults(apps, schema_editor):
    Exam = apps.get_model('school', 'Exam')
    defaults = {
        'weekly_test': (10, Decimal('5.00')),
        'monthly_test': (20, Decimal('10.00')),
        'quarterly_test': (30, Decimal('15.00')),
        'mid_term': (40, Decimal('25.00')),
        'pre_final': (50, Decimal('20.00')),
        'final': (60, Decimal('25.00')),
    }
    for exam in Exam.objects.all():
        if not getattr(exam, 'exam_type', None):
            exam.exam_type = 'monthly_test'
        sequence, weight = defaults.get(exam.exam_type, defaults['monthly_test'])
        if not getattr(exam, 'sequence', None):
            exam.sequence = sequence
        if not getattr(exam, 'result_weight', None):
            exam.result_weight = weight
        if not getattr(exam, 'academic_year', None):
            year = exam.start_date.year if exam.start_date else 2026
            exam.academic_year = str(year)
        exam.save(update_fields=['exam_type', 'sequence', 'result_weight', 'academic_year'])


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0050_admin_profile_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='academic_year',
            field=models.CharField(default='2026', max_length=20),
        ),
        migrations.AddField(
            model_name='exam',
            name='exam_type',
            field=models.CharField(choices=[('weekly_test', 'Weekly Test'), ('monthly_test', 'Monthly Test'), ('quarterly_test', 'Quarterly Test'), ('mid_term', 'Mid Term Exam'), ('pre_final', 'Pre Final Exam'), ('final', 'Final Exam')], default='monthly_test', max_length=30),
        ),
        migrations.AddField(
            model_name='exam',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='exam',
            name='result_weight',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=5),
        ),
        migrations.AddField(
            model_name='exam',
            name='sequence',
            field=models.PositiveSmallIntegerField(default=20),
        ),
        migrations.AddField(
            model_name='exam',
            name='term_label',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.CreateModel(
            name='ExamDateSheetItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_date', models.DateField()),
                ('start_time', models.TimeField(default='09:00')),
                ('end_time', models.TimeField(default='12:00')),
                ('room', models.CharField(blank=True, max_length=80)),
                ('instructions', models.CharField(blank=True, max_length=255)),
                ('sort_order', models.PositiveSmallIntegerField(default=1)),
                ('exam_subject', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='date_sheet_item', to='school.examsubject')),
            ],
            options={
                'ordering': ['paper_date', 'start_time', 'sort_order', 'exam_subject__subject__name'],
                'indexes': [models.Index(fields=['paper_date'], name='exam_datesheet_date_idx'), models.Index(fields=['sort_order'], name='exam_datesheet_order_idx')],
            },
        ),
        migrations.RunPython(set_exam_schema_defaults, migrations.RunPython.noop),
        migrations.AddIndex(
            model_name='exam',
            index=models.Index(fields=['academic_year', 'grade', 'exam_type'], name='exam_year_grade_type_idx'),
        ),
        migrations.AddIndex(
            model_name='exam',
            index=models.Index(fields=['sequence'], name='exam_sequence_idx'),
        ),
        migrations.AddIndex(
            model_name='exam',
            index=models.Index(fields=['is_locked'], name='exam_locked_idx'),
        ),
        migrations.AddConstraint(
            model_name='exam',
            constraint=models.UniqueConstraint(fields=('academic_year', 'grade', 'exam_type', 'name'), name='unique_exam_schema_per_grade_year'),
        ),
    ]
