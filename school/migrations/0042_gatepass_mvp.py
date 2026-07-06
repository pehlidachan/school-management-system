from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0041_online_requests'),
    ]

    operations = [
        migrations.CreateModel(
            name='GatePass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_type', models.CharField(choices=[('student', 'Student'), ('staff', 'Staff Member'), ('worker', 'Maintenance Worker'), ('other', 'Other Visitor')], default='student', max_length=20)),
                ('person_name', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=100)),
                ('organization', models.CharField(blank=True, max_length=255)),
                ('destination', models.CharField(blank=True, max_length=255)),
                ('reason', models.TextField()),
                ('luggage_detail', models.TextField(blank=True)),
                ('expected_return_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('issued', 'Issued'), ('returned', 'Returned'), ('cancelled', 'Cancelled')], default='issued', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('returned_at', models.DateTimeField(blank=True, null=True)),
                ('issued_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='issued_gate_passes', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gate_passes', to='school.staff')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gate_passes', to='school.student')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
