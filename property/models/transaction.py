from django.db import models
from .property import Property



class Transaction(models.Model):
    TRANSACTIONS_TYPE = [('sale', 'Sale'), ('rent', 'Rent')]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_transaction')
    transaction_type = models.CharField(max_length=50, choices=TRANSACTIONS_TYPE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='buyer_transaction')
    seller = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='seller_transaction')
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return self.property.title
