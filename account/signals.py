from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import FollowUser, Profile, Gender


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Gender.objects.create(user=instance)


@receiver(post_save, sender=FollowUser)
def add_follower(sender, instance, created, **kwargs):
    if created:
        # add notification item
        pass
