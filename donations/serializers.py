from django.utils import timezone
from rest_framework import serializers
from .models import DonationRequest, Donation

class DonationRequestSerializer(serializers.ModelSerializer):
    remaining_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    beneficiary_name = serializers.CharField(
        source='beneficiary.email',
        read_only=True
    )
    beneficiary = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = DonationRequest
        fields = [
            'id', 'title', 'description', 'category', 'target_amount',
            'collected_amount', 'remaining_amount', 'deadline', 'status',
            'created_at', 'beneficiary', 'beneficiary_name'
        ]
        read_only_fields = ['collected_amount', 'status', 'beneficiary']

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Deadline must be in the future.")
        return value

class DonationSerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(
        source='donor.email',
        read_only=True
    )

    class Meta:
        model = Donation
        fields = ['id', 'donation_request', 'amount', 'created_at', 'donor_name']
        read_only_fields = ['donor']