from rest_framework import serializers
from ..models import VisitBooking


class VisitBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitBooking
        fields = ('property', 'user', 'status', 'booking_date', 'created_at')
