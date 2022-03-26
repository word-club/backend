from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from comment.helper import (
    add_pub_discussions,
    decrease_pub_discussions,
)
from comment.models import Comment
from helpers.update_reactions import notify_author


@receiver(post_save, sender=Comment)
def post_save_comment(sender, instance, created, **kwargs):
    add_pub_discussions(instance, created)
    if created:
        notify_author(
            target=instance.publication, instance=instance, key="comment", verb="commented"
        )


@receiver(post_delete, sender=Comment)
def post_delete_comment(sender, instance, **kwargs):
    decrease_pub_discussions(instance)
