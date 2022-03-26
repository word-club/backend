from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from helpers.update_reactions import (
    add_popularity,
    add_supports,
    decrease_popularity,
    decrease_supports,
)
from helpers.notify import notify_author
from share.models import Share


@receiver(post_save, sender=Share)
def post_save_pub_share(sender, instance, created, **kwargs):
    if created:
        add_popularity(instance)
        add_supports(instance)
        shared_instance = instance.profile or instance.publication or instance.comment
        notify_author(shared_instance, instance, "shared")


@receiver(post_delete, sender=Share)
def post_delete_pub_share(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)
