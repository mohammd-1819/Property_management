from django.contrib import admin
from .models import City, Owner, Property, Transaction, VisitBooking

admin.site.register(City)
admin.site.register(Owner)
admin.site.register(Property)
admin.site.register(Transaction)
admin.site.register(VisitBooking)
