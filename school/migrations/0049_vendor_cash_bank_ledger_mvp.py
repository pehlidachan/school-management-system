# Generated for vendor and cash bank ledger MVP on 2026-07-07

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0048_study_material_center'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=180)),
                ('phone', models.CharField(blank=True, max_length=80)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('note', models.TextField(blank=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name'], 'indexes': [models.Index(fields=['status'], name='school_vend_status_9b1627_idx')]},
        ),
        migrations.CreateModel(
            name='CashBankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('account_type', models.CharField(choices=[('cash', 'Cash'), ('bank', 'Bank')], default='cash', max_length=20)),
                ('opening_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['account_type', 'name'], 'indexes': [models.Index(fields=['account_type'], name='school_cash_account_70f2e9_idx'), models.Index(fields=['status'], name='school_cash_status_e79a40_idx')]},
        ),
        migrations.CreateModel(
            name='VendorLedgerEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField(default=django.utils.timezone.localdate)),
                ('description', models.CharField(max_length=220)),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('payment_method', models.CharField(blank=True, max_length=80)),
                ('note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_vendor_ledger_entries', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ledger_entries', to='school.vendor')),
            ],
            options={'ordering': ['-entry_date', '-created_at'], 'indexes': [models.Index(fields=['entry_date'], name='school_vend_entry_d_06a5ef_idx'), models.Index(fields=['vendor', 'entry_date'], name='school_vend_vendor__79d79e_idx')]},
        ),
        migrations.CreateModel(
            name='CashBankTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField(default=django.utils.timezone.localdate)),
                ('title', models.CharField(max_length=180)),
                ('transaction_type', models.CharField(choices=[('income', 'Income'), ('expense', 'Expense'), ('transfer', 'Transfer')], default='expense', max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='school.cashbankaccount')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_cash_bank_transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-transaction_date', '-created_at'], 'indexes': [models.Index(fields=['transaction_date'], name='school_cash_transac_3fb9bb_idx'), models.Index(fields=['account', 'transaction_type'], name='school_cash_account_e9f9ee_idx')]},
        ),
    ]
