from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import DonationRequest, Donation
from .serializers import (
    DonationRequestSerializer,
    DonationSerializer,
    DonationActionSerializer
)


class DonationRequestViewSet(viewsets.ModelViewSet):
    serializer_class = DonationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = DonationRequest.objects.filter(status='ACTIVE')
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def perform_create(self, serializer):
        serializer.save(beneficiary=self.request.user)

    @action(detail=True, methods=['post'])
    def donate(self, request, pk=None):
        """
        Make a donation to this request.
        """
        donation_request = self.get_object()

        # Use the new serializer for validation
        serializer = DonationActionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        amount = serializer.validated_data['amount']

        # Check if the donation request is active
        if donation_request.status != 'ACTIVE':
            return Response(
                {'error': 'This donation request is not active'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create donation
        donation = Donation.objects.create(
            donor=request.user,
            donation_request=donation_request,
            amount=amount
        )

        return Response({
            'status': 'success',
            'message': f'Successfully donated {amount} to {donation_request.title}',
            'remaining_amount': donation_request.remaining_amount()
        }, status=status.HTTP_201_CREATED)