from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from vote.models import Vote
from helpers.vote_signals import (
    add_popularity,
    add_supports,
    notify_author,
    decrease_popularity,
    decrease_supports
)


@receiver(post_save, sender=Vote)
def post_save_vote(sender, instance, created, **kwargs):
    add_popularity(instance)
    add_supports(instance)
    notify_author(instance)


@receiver(post_delete, sender=Vote)
def post_delete_vote(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)
