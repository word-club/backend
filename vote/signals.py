from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from helpers.update_reactions import (
    add_popularity,
    add_supports,
    decrease_popularity,
    decrease_supports,
)
from helpers.notify import notify_author
from vote.models import Vote


@receiver(post_save, sender=Vote)
def post_save_vote(sender, instance, created, **kwargs):
    add_popularity(instance)
    add_supports(instance)
    voted_instance = instance.publication or instance.comment
    verb = f"{'up' if instance.up else 'down'}-voted"
    notify_author(voted_instance, instance, verb)


@receiver(pre_delete, sender=Vote)
def post_delete_vote(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)
