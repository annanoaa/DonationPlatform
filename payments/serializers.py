from rest_framework import serializers
from .models import BankAccount, Transaction

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'account_number', 'bank_name', 'account_holder_name',
                 'is_verified', 'created_at']
        read_only_fields = ['is_verified', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'donation', 'from_account', 'to_account', 'amount',
                 'status', 'bank_reference', 'initiated_at', 'completed_at']
        read_only_fields = ['status', 'bank_reference', 'initiated_at',
                           'completed_at']