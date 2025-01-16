from django.db import models
# from account.models import User


class Owner(models.Model):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
