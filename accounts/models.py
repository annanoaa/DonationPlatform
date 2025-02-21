from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('DONOR', 'Donor'),
        ('BENEFICIARY', 'Beneficiary'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='DONOR')
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)  # Demo balance
    phone_number = models.CharField(max_length=15, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email