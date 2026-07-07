# Generated for CodeRabbit safety review on 2026-07-07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0045_rename_school_indexes_and_sync_model_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='monthly_fee',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
    ]
