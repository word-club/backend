from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from publication.models import (
    PublicationBookmark,
    HidePublication,
)


@receiver(post_save, sender=PublicationBookmark)
def post_save_pub_bookmark(sender, instance, created, **kwargs):
    add_popularity(instance, created)
    add_supports(instance, created)
    notify_author(instance, created)


@receiver(post_save, sender=HidePublication)
def post_save_pub_hide(sender, instance, created, **kwargs):
    add_dislikes(instance, created)

@receiver(post_save, sender=PublicationBookmark)
def post_delete_pub_bookmark(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)


@receiver(post_save, sender=HidePublication)
def post_delete_pub_hide(sender, instance, **kwargs):
    decrease_dislikes(instance)
