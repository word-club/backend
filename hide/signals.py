from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from helpers.vote_signals import add_dislikes, decrease_dislikes
from hide.models import Hide


@receiver(post_save, sender=Hide)
def post_save_hide(sender, instance, created, **kwargs):
    add_dislikes(instance)


@receiver(post_delete, sender=Hide)
def post_delete_hide(sender, instance, **kwargs):
    decrease_dislikes(instance)
