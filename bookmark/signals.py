from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from bookmark.helper import (
    add_popularity,
    add_supports,
    decrease_popularity,
    decrease_supports,
)
from bookmark.models import Bookmark


@receiver(post_save, sender=Bookmark)
def post_save_bookmark(sender, instance, created, **kwargs):
    if created:
        add_popularity(instance)
        add_supports(instance)


@receiver(post_delete, sender=Bookmark)
def post_delete_bookmark(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)
