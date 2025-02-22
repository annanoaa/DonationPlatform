from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

def generate_unique_username():
    return f"user_{uuid.uuid4().hex[:8]}"

class User(AbstractUser):
    email = models.EmailField(unique=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        default=generate_unique_username
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email