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

    @action(detail=True, methods=['post'])
    def donate(self, request, pk=None):
        donation_request = self.get_object()

        # Validate the amount
        try:
            amount = float(request.data.get('amount', 0))
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

        # Create donation
        donation = Donation(
            donor=request.user,
            donation_request=donation_request,
            amount=amount
        )

        try:
            donation.save()
            return Response({
                'status': 'success',
                'message': f'Successfully donated {amount} to {donation_request.title}',
                'remaining_amount': donation_request.remaining_amount()
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )