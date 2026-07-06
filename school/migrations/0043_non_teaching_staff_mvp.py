from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('school', '0042_gatepass_mvp'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonTeachingStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('appointment', models.CharField(max_length=255)),
                ('work_detail', models.TextField(blank=True)),
                ('department', models.CharField(blank=True, max_length=255)),
                ('qualification', models.CharField(blank=True, max_length=255)),
                ('experience', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(max_length=100)),
                ('emergency_phone', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=500)),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('salary', models.CharField(blank=True, max_length=50)),
                ('contract_details', models.TextField(blank=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employment_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.employmentstatus')),
                ('gender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.gender')),
            ],
            options={'ordering': ['name']},
        ),
    ]
