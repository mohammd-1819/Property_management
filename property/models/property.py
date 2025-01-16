from django.db import models
from .owner import Owner
from .city import City


class Property(models.Model):
    PROPERTY_TYPE = [('apartment', 'Apartment'), ('house', 'House'), ('land', 'Land')]
    AVAILABILITY = [('sale', 'For Sale'), ('rent', 'For Rent')]

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='property')
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='property')
    price = models.DecimalField(max_digits=10, decimal_places=0)
    size = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    garage = models.BooleanField(default=True)
    availability = models.CharField(max_length=50, choices=AVAILABILITY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='property/img', null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.owner.user.role == 'user':
            self.owner.user.role = 'owner'
            self.owner.save()

    class Meta:
        verbose_name = 'property'
        verbose_name_plural = 'properties'
