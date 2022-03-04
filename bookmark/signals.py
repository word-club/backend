from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from bookmark.models import Bookmark
from helpers.vote_signals import (add_popularity, add_supports,
                                  decrease_popularity, decrease_supports,
                                  notify_author)


@receiver(post_save, sender=Bookmark)
def post_save_bookmark(sender, instance, created, **kwargs):
    add_popularity(instance)
    add_supports(instance)
    notify_author(instance)


@receiver(post_delete, sender=Bookmark)
def post_delete_bookmark(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)
