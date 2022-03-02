from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from publication.models import (
    HidePublication,
)


@receiver(post_save, sender=HidePublication)
def post_save_pub_hide(sender, instance, created, **kwargs):
    add_dislikes(instance, created)


@receiver(post_save, sender=HidePublication)
def post_delete_pub_hide(sender, instance, **kwargs):
    decrease_dislikes(instance)
