from rest_framework import serializers
from .models import DonationRequest, Donation

class DonationRequestSerializer(serializers.ModelSerializer):
    remaining_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    beneficiary_name = serializers.CharField(
        source='beneficiary.get_full_name',
        read_only=True
    )

    class Meta:
        model = DonationRequest
        fields = [
            'id', 'title', 'description', 'category', 'target_amount',
            'collected_amount', 'remaining_amount', 'deadline', 'status',
            'created_at', 'beneficiary_name'
        ]
        read_only_fields = ['collected_amount', 'status']

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'donation_request', 'amount', 'created_at']
        read_only_fields = ['donor']