from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from comment.models import (
    Comment,
    CommentUpVote,
    CommentDownVote,
    CommentShare,
    CommentBookmark,
    HideComment,
)
from comment.signals.helper import *


@receiver(post_save, sender=Comment)
def post_save_comment(sender, instance, created, **kwargs):
    add_pub_discussions(instance, created)


@receiver(post_delete, sender=Comment)
def post_delete_comment(sender, instance, **kwargs):
    decrease_pub_discussions(instance)


@receiver(post_save, sender=CommentUpVote)
def post_save_up_vote(sender, instance, created, **kwargs):
    add_popularity(instance, created)


@receiver(post_save, sender=CommentDownVote)
def post_save_down_vote(sender, instance, created, **kwargs):
    add_popularity(instance, created)
    add_dislikes(instance, created)


@receiver(post_save, sender=CommentShare)
def post_save_share(sender, instance, created, **kwargs):
    add_popularity(instance, created)
    add_supports(instance, created)


@receiver(post_save, sender=CommentBookmark)
def post_save_bookmark(sender, instance, created, **kwargs):
    add_popularity(instance, created)
    add_supports(instance, created)


@receiver(post_save, sender=HideComment)
def post_save_hide(sender, instance, created, **kwargs):
    add_dislikes(instance, created)


@receiver(post_delete, sender=CommentUpVote)
def post_delete_up_vote(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)


@receiver(post_delete, sender=CommentDownVote)
def post_delete_down_vote(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_dislikes(instance)


@receiver(post_delete, sender=CommentShare)
def post_delete_share(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)


@receiver(post_save, sender=CommentBookmark)
def post_delete_bookmark(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)


@receiver(post_save, sender=HideComment)
def post_delete_hide(sender, instance, **kwargs):
    decrease_dislikes(instance)
