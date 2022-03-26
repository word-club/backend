from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from comment.models import Comment
from helpers.notify import notify_author
from helpers.update_reactions import add_discussions, decrease_discussions


@receiver(post_save, sender=Comment)
def post_save_comment(sender, instance, created, **kwargs):
    if created:
        add_discussions(instance)
        if getattr(instance, "author", None) is not None:
            notify_author(target=instance.publication, instance=instance, verb="commented")


@receiver(post_delete, sender=Comment)
def post_delete_comment(sender, instance, **kwargs):
    decrease_discussions(instance)
