from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from comment.models import (
    Comment,
    HideComment,
)
from comment.signal_helper import *


@receiver(post_save, sender=Comment)
def post_save_comment(sender, instance, created, **kwargs):
    add_pub_discussions(instance, created)
    notify_post_subscribers(instance, created)


@receiver(post_delete, sender=Comment)
def post_delete_comment(sender, instance, **kwargs):
    decrease_pub_discussions(instance)


@receiver(post_save, sender=HideComment)
def post_save_hide(sender, instance, created, **kwargs):
    add_dislikes(instance, created)


@receiver(post_save, sender=HideComment)
def post_delete_hide(sender, instance, **kwargs):
    decrease_dislikes(instance)
