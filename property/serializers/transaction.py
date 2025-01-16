from rest_framework import serializers
from ..models import Transaction, Property
from account.models import User


class TransactionSerializer(serializers.ModelSerializer):
    property = serializers.SlugRelatedField(slug_field='title', queryset=Property.objects.all())
    buyer = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    seller = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Transaction
        fields = ('property', 'transaction_type', 'transaction_date', 'buyer', 'seller', 'price')
