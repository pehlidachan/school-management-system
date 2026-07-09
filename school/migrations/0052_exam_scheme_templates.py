from decimal import Decimal

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def seed_scheme_one(apps, schema_editor):
    ExamScheme = apps.get_model('school', 'ExamScheme')
    ExamSchemeItem = apps.get_model('school', 'ExamSchemeItem')
    Exam = apps.get_model('school', 'Exam')

    scheme, _ = ExamScheme.objects.get_or_create(
        code='scheme-1',
        defaults={
            'name': 'Scheme 1',
            'description': 'Default school exam scheme: Weekly, Monthly, Quarterly, Mid Term, Pre Final and Final Exam.',
            'is_default': True,
            'is_active': True,
        },
    )

    rows = [
        ('weekly_test', 'Weekly Test', 10, Decimal('5.00'), Decimal('100.00'), Decimal('33.00'), True, False),
        ('monthly_test', 'Monthly Test', 20, Decimal('10.00'), Decimal('100.00'), Decimal('33.00'), True, False),
        ('quarterly_test', 'Quarterly Test', 30, Decimal('15.00'), Decimal('100.00'), Decimal('33.00'), True, False),
        ('mid_term', 'Mid Term Exam', 40, Decimal('25.00'), Decimal('100.00'), Decimal('33.00'), True, True),
        ('pre_final', 'Pre Final Exam', 50, Decimal('20.00'), Decimal('100.00'), Decimal('33.00'), True, True),
        ('final', 'Final Exam', 60, Decimal('25.00'), Decimal('100.00'), Decimal('33.00'), True, True),
    ]

    item_map = {}
    for key, name, sequence, weight, total, passing, include, major in rows:
        item, _ = ExamSchemeItem.objects.get_or_create(
            scheme=scheme,
            item_key=key,
            defaults={
                'display_name': name,
                'sequence': sequence,
                'result_weight': weight,
                'default_total_marks': total,
                'default_passing_marks': passing,
                'include_in_final_result': include,
                'is_major_exam': major,
                'is_active': True,
            },
        )
        item_map[key] = item

    for exam in Exam.objects.all():
        exam.scheme = scheme
        exam.scheme_item = item_map.get(exam.exam_type)
        exam.save(update_fields=['scheme', 'scheme_item'])


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0051_exam_fixed_schema'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamScheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Scheme 1', max_length=120)),
                ('code', models.SlugField(default='scheme-1', max_length=80, unique=True)),
                ('description', models.TextField(blank=True)),
                ('is_default', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_exam_schemes', to=settings.AUTH_USER_MODEL)),
                ('school_brand', models.ForeignKey(blank=True, help_text='Optional. Attach this scheme to a specific school/tenant in future SaaS mode.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exam_schemes', to='school.schoolbrandprofile')),
            ],
            options={
                'ordering': ['-is_default', 'name'],
                'indexes': [models.Index(fields=['code'], name='exam_scheme_code_idx'), models.Index(fields=['is_active'], name='exam_scheme_active_idx'), models.Index(fields=['is_default'], name='exam_scheme_default_idx')],
            },
        ),
        migrations.CreateModel(
            name='ExamSchemeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_key', models.SlugField(max_length=80)),
                ('display_name', models.CharField(max_length=120)),
                ('sequence', models.PositiveSmallIntegerField(default=20)),
                ('result_weight', models.DecimalField(decimal_places=2, default=10, max_digits=5)),
                ('default_total_marks', models.DecimalField(decimal_places=2, default=100, max_digits=7)),
                ('default_passing_marks', models.DecimalField(decimal_places=2, default=33, max_digits=7)),
                ('include_in_final_result', models.BooleanField(default=True)),
                ('is_major_exam', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='school.examscheme')),
            ],
            options={
                'ordering': ['scheme', 'sequence', 'display_name'],
                'indexes': [models.Index(fields=['scheme', 'sequence'], name='exam_scheme_item_order_idx'), models.Index(fields=['is_active'], name='exam_scheme_item_active_idx')],
                'constraints': [models.UniqueConstraint(fields=('scheme', 'item_key'), name='unique_item_per_exam_scheme')],
            },
        ),
        migrations.AddField(
            model_name='exam',
            name='scheme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exams', to='school.examscheme'),
        ),
        migrations.AddField(
            model_name='exam',
            name='scheme_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exams', to='school.examschemeitem'),
        ),
        migrations.RemoveConstraint(
            model_name='exam',
            name='unique_exam_schema_per_grade_year',
        ),
        migrations.AddIndex(
            model_name='exam',
            index=models.Index(fields=['scheme', 'academic_year', 'grade'], name='exam_scheme_year_grade_idx'),
        ),
        migrations.AddConstraint(
            model_name='exam',
            constraint=models.UniqueConstraint(fields=('scheme', 'academic_year', 'grade', 'exam_type', 'name'), name='unique_exam_scheme_per_grade_year'),
        ),
        migrations.RunPython(seed_scheme_one, migrations.RunPython.noop),
    ]
