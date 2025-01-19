from rest_framework import serializers
from ..models import VisitBooking, Property
from account.models import User


class VisitBookingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    property = serializers.SlugRelatedField(slug_field='title', queryset=Property.objects.all())

    class Meta:
        model = VisitBooking
        fields = ('property', 'user', 'status', 'booking_date', 'created_at')


class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitBooking
        fields = ('property', 'booking_date')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
