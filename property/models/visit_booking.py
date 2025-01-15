from django.db import models
from .property import Property
# from account import User
from account.models import User


class VisitBooking(models.Model):
    STATUS = [('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='booking')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking')
    status = models.CharField(max_length=50, choices=STATUS, default='pending')
    booking_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booking for {self.property.title}"
