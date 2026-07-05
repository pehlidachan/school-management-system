from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('school', '0040_results_mvp')]
    operations = [
        migrations.CreateModel(
            name='ParentComplaint',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('parent_name', models.CharField(max_length=255)),
                ('student_name', models.CharField(max_length=255)),
                ('student_class', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('status', models.CharField(default='new', max_length=20)),
                ('admin_note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='OnlineAdmissionApplication',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('student_name', models.CharField(max_length=255)),
                ('desired_class', models.CharField(max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=50)),
                ('father_name', models.CharField(max_length=255)),
                ('guardian_phone', models.CharField(max_length=100)),
                ('guardian_email', models.EmailField(blank=True, max_length=254)),
                ('previous_school', models.CharField(blank=True, max_length=255)),
                ('address', models.TextField()),
                ('note', models.TextField(blank=True)),
                ('status', models.CharField(default='new', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('applicant_name', models.CharField(max_length=255)),
                ('applied_for', models.CharField(max_length=255)),
                ('qualification', models.CharField(max_length=255)),
                ('experience', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address', models.TextField(blank=True)),
                ('cover_note', models.TextField(blank=True)),
                ('status', models.CharField(default='new', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
