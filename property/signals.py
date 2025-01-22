from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from .models import Property, VisitBooking


@receiver([post_save, post_delete], sender=Property)
def clear_property_cache(sender, **kwargs):
    for page in range(1, 100):
        cache.delete(f'property_list_page_{page}')


@receiver([post_save, post_delete], sender=Property)
def clear_user_property_cache(sender, instance, **kwargs):
    if instance.owner and instance.owner.user:
        user_id = instance.owner.user.id
        for page in range(1, 100):
            cache.delete(f'user_property_list_page_{page}_user_{user_id}')


@receiver([post_save, post_delete], sender=VisitBooking)
def clear_booking_cache(sender, **kwargs):
    for page in range(1, 100):
        cache.delete(f'booking_list_page_{page}')
