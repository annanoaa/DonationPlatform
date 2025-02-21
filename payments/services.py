import uuid
from datetime import datetime
from decimal import Decimal
from django.conf import settings
from django.db import transaction
from .models import Transaction, BankAccount


class BankAPIService:
    """
    Service class for bank API integration.
    Replace the mock methods with actual bank API calls in production.
    """

    @staticmethod
    def generate_bank_reference():
        return f"TR-{uuid.uuid4().hex[:12].upper()}"

    @staticmethod
    def verify_account(account_number: str) -> bool:
        """
        Verify if bank account exists and is valid.
        Replace with actual bank API call.
        """
        try:
            return BankAccount.objects.filter(
                account_number=account_number,
                is_verified=True
            ).exists()
        except Exception as e:
            raise Exception(f"Bank API Error: {str(e)}")

    @staticmethod
    def check_balance(account: BankAccount) -> Decimal:
        """
        Check account balance.
        Replace with actual bank API call.
        """
        try:
            # Simulate bank API call
            return account.balance
        except Exception as e:
            raise Exception(f"Bank API Error: {str(e)}")

    @classmethod
    @transaction.atomic
    def process_transaction(cls, transaction: Transaction) -> bool:
        """
        Process the bank transaction.
        Replace with actual bank API integration.
        """
        try:
            # Verify accounts
            if not (cls.verify_account(transaction.from_account.account_number) and
                    cls.verify_account(transaction.to_account.account_number)):
                raise ValueError("Invalid account(s)")

            # Check balance
            if cls.check_balance(transaction.from_account) < transaction.amount:
                raise ValueError("Insufficient funds")

            # Update transaction status
            transaction.status = 'PROCESSING'
            transaction.save()

            # Simulate bank transfer
            with transaction.atomic():
                # Deduct from sender
                transaction.from_account.balance -= transaction.amount
                transaction.from_account.save()

                # Add to receiver
                transaction.to_account.balance += transaction.amount
                transaction.to_account.save()

                # Update transaction status
                transaction.status = 'COMPLETED'
                transaction.completed_at = datetime.now()
                transaction.save()

            return True

        except Exception as e:
            transaction.status = 'FAILED'
            transaction.failure_reason = str(e)
            transaction.save()
            raise Exception(f"Transaction failed: {str(e)}")