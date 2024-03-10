from rest_framework import serializers

from accounting.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'profile', 'description', 'credit', 'debit', 'billing_cycle', 'created_at')
        read_only_fields = fields
