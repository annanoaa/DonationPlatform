from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)  # Demo balance

    # Make username optional
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove username from required fields

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email