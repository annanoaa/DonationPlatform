from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import DonationRequest, Donation
from .serializers import DonationRequestSerializer, DonationSerializer


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
        # Set the beneficiary as the current authenticated user
        serializer.save(beneficiary=self.request.user)

    @action(detail=True, methods=['post'])
    def donate(self, request, pk=None):
        donation_request = self.get_object()

        amount = request.data.get('amount')
        if not amount:
            return Response(
                {'error': 'Amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = float(amount)
            if amount <= 0:
                return Response(
                    {'error': 'Amount must be greater than 0'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (TypeError, ValueError):
            return Response(
                {'error': 'Invalid amount'},
                status=status.HTTP_400_BAD_REQUEST
            )

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