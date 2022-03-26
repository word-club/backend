from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from helpers.update_reactions import (
    add_popularity,
    add_supports,
    decrease_popularity,
    decrease_supports,
)
from bookmark.models import Bookmark
from helpers.notify import notify_author


@receiver(post_save, sender=Bookmark)
def post_save_bookmark(instance, created, **kwargs):
    if created:
        add_popularity(instance)
        add_supports(instance)
        # exclude community notification for bookmark creation
        target = instance.profile or instance.publication or instance.comment
        if target:
            notify_author(target=target, instance=instance, verb="bookmarked")


@receiver(post_delete, sender=Bookmark)
def post_delete_bookmark(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)
