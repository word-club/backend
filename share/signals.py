from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from share.models import Share
from helpers.vote_signals import (
    add_popularity,
    add_supports,
    notify_author,
    decrease_popularity,
    decrease_supports,
)


@receiver(post_save, sender=Share)
def post_save_pub_share(sender, instance, created, **kwargs):
    if created:
        add_popularity(instance)
        add_supports(instance)
        notify_author(instance)


@receiver(post_delete, sender=Share)
def post_delete_pub_share(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)
