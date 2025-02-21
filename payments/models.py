from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from donations.models import Donation
from decimal import Decimal

class BankAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=30, unique=True)
    bank_name = models.CharField(max_length=100)
    account_holder_name = models.CharField(max_length=200)
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"

    class Meta:
        indexes = [
            models.Index(fields=['account_number']),
            models.Index(fields=['user']),
        ]

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REVERSED', 'Reversed')
    ]

    donation = models.OneToOneField(
        Donation,
        on_delete=models.CASCADE,
        related_name='transaction'
    )
    from_account = models.ForeignKey(
        BankAccount,
        on_delete=models.PROTECT,
        related_name='sent_transactions'
    )
    to_account = models.ForeignKey(
        BankAccount,
        on_delete=models.PROTECT,
        related_name='received_transactions'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    bank_reference = models.CharField(max_length=100, unique=True)
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['bank_reference']),
            models.Index(fields=['status']),
            models.Index(fields=['initiated_at']),
        ]

    def __str__(self):
        return f"Transaction {self.bank_reference} - {self.status}"