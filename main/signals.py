from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import User, Profile
from .utils import generate_address

@receiver(post_save, sender=User)
def create_profile_signal(sender, instance, created, **kwargs):

    """
    A signal responsible for creating profiles automatically when a new user is created
    """

    if created:
        address = generate_address(instance.id)
        Profile.objects.create(user=instance, address=address)


@receiver(post_delete, sender=Profile)
def delete_user_on_profile_delete(sender, instance, **kwargs):

    """
    A signal responsible for deleting users automatically when a profile is deleted
    """
    
    instance.user.delete()
