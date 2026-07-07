# Generated manually from WhatsApp ERP MVP gap analysis on 2026-07-07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0043_non_teaching_staff_mvp'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='gr_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='admission_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='roll_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='student_name_urdu',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='father_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='guardian_cnic',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='rejoining_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='mother_mobile',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='whatsapp_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='blood_group',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='fee_category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='monthly_fee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='student',
            name='welcome_card_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='welcome_card_sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='photo_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='staff_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='staff_name_urdu',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='father_or_husband_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='cnic',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='whatsapp_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='rejoining_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='can_print_student_biodata',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='can_print_staff_biodata',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='birthday_card_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='photo_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
