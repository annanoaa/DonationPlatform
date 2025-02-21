from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import BankAccount, Transaction
from .serializers import BankAccountSerializer, TransactionSerializer
from .services import BankAPIService
from donations.models import Donation


class BankAccountViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BankAccountSerializer

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(
            from_account__user=self.request.user
        )

    @action(detail=False, methods=['post'])
    def process_donation(self, request):
        try:
            donation_id = request.data.get('donation_id')
            donation = get_object_or_404(Donation, id=donation_id)

            # Get donor's bank account
            from_account = get_object_or_404(
                BankAccount,
                user=request.user,
                is_verified=True
            )

            # Get beneficiary's bank account
            to_account = get_object_or_404(
                BankAccount,
                user=donation.donation_request.beneficiary,
                is_verified=True
            )

            # Create transaction
            transaction = Transaction.objects.create(
                donation=donation,
                from_account=from_account,
                to_account=to_account,
                amount=donation.amount,
                bank_reference=BankAPIService.generate_bank_reference()
            )

            # Process the transaction
            BankAPIService.process_transaction(transaction)

            return Response({
                'status': 'success',
                'message': 'Transaction processed successfully',
                'transaction': TransactionSerializer(transaction).data
            })

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)