# Generated by Django 5.1.6 on 2025-02-21 18:28

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('donations', '0002_alter_donationrequest_category_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=30, unique=True)),
                ('bank_name', models.CharField(max_length=100)),
                ('account_holder_name', models.CharField(max_length=200)),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed'), ('REVERSED', 'Reversed')], default='PENDING', max_length=20)),
                ('bank_reference', models.CharField(max_length=100, unique=True)),
                ('initiated_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('failure_reason', models.TextField(blank=True)),
                ('donation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='donations.donation')),
                ('from_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sent_transactions', to='payments.bankaccount')),
                ('to_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='received_transactions', to='payments.bankaccount')),
            ],
        ),
        migrations.AddIndex(
            model_name='bankaccount',
            index=models.Index(fields=['account_number'], name='payments_ba_account_172ef2_idx'),
        ),
        migrations.AddIndex(
            model_name='bankaccount',
            index=models.Index(fields=['user'], name='payments_ba_user_id_501ece_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['bank_reference'], name='payments_tr_bank_re_10d6b8_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['status'], name='payments_tr_status_96e6c0_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['initiated_at'], name='payments_tr_initiat_ca85b2_idx'),
        ),
    ]
