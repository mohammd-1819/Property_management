from rest_framework import serializers
from ..models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('property', 'transaction_type', 'transaction_date', 'buyer', 'seller', 'price')

