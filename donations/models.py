from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone

class DonationRequest(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled')
    ]

    CATEGORY_CHOICES = [
        ('ANIMALS', 'Homeless Animals'),
        ('CHARITY', 'Charity'),
        ('ECOSYSTEM', 'Ecosystem'),
        ('MEDICAL', 'Medical Help'),
        ('EDUCATION', 'Education'),
        ('OTHER', 'Other')
    ]

    beneficiary = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donation_requests'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='OTHER'
    )
    target_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    collected_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def remaining_amount(self):
        return max(0, self.target_amount - self.collected_amount)

    def is_expired(self):
        return timezone.now() > self.deadline

    def save(self, *args, **kwargs):
        if self.is_expired() and self.status == 'ACTIVE':
            self.status = 'EXPIRED'
        if self.collected_amount >= self.target_amount and self.status == 'ACTIVE':
            self.status = 'COMPLETED'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.beneficiary.email}"

class Donation(models.Model):
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donations_made'
    )
    donation_request = models.ForeignKey(
        DonationRequest,
        on_delete=models.CASCADE,
        related_name='donations'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.donor == self.donation_request.beneficiary:
            raise ValidationError("Beneficiaries cannot donate to their own requests.")
        if self.donation_request.status != 'ACTIVE':
            raise ValidationError("Cannot donate to non-active requests.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        # Update the collected amount in the donation request
        self.donation_request.collected_amount += self.amount
        self.donation_request.save()

    def __str__(self):
        return f"{self.donor.email} donated {self.amount} to {self.donation_request.title}"