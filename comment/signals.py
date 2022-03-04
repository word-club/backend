from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from comment.models import Comment
from comment.signal_helper import *


@receiver(post_save, sender=Comment)
def post_save_comment(sender, instance, created, **kwargs):
    add_pub_discussions(instance, created)
    notify_post_subscribers(instance, created)


@receiver(post_delete, sender=Comment)
def post_delete_comment(sender, instance, **kwargs):
    decrease_pub_discussions(instance)
