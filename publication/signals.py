from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from publication.models import (
    PublicationUpVote,
    PublicationDownVote,
    PublicationShare,
    PublicationBookmark,
    HidePublication,
)


def add_popularity(instance, created):
    if created:
        instance.publication.popularity += 1
        instance.publication.save()


def add_dislikes(instance, created):
    if created:
        instance.publication.dislikes += 1
        instance.publication.save()


def add_supports(instance, created):
    if created:
        instance.publication.supports += 1
        instance.publication.save()


def decrease_popularity(instance):
    instance.publication.popularity -= 1
    instance.publication.save()


def decrease_dislikes(instance):
    instance.publication.dislikes -= 1
    instance.publication.save()


def decrease_supports(instance):
    instance.publication.supports -= 1
    instance.publication.save()


@receiver(post_save, sender=PublicationUpVote)
def post_save_pub_up_vote(sender, instance, created, **kwargs):
    add_popularity(instance, created)
    add_supports(instance, created)


@receiver(post_save, sender=PublicationDownVote)
def post_save_pub_down_vote(sender, instance, created, **kwargs):
    add_popularity(instance, created)
    add_dislikes(instance, created)


@receiver(post_save, sender=PublicationShare)
def post_save_pub_share(sender, instance, created, **kwargs):
    add_popularity(instance, created)
    add_supports(instance, created)


@receiver(post_save, sender=PublicationBookmark)
def post_save_pub_bookmark(sender, instance, created, **kwargs):
    add_popularity(instance, created)
    add_supports(instance, created)


@receiver(post_save, sender=HidePublication)
def post_save_pub_hide(sender, instance, created, **kwargs):
    add_dislikes(instance, created)


@receiver(post_delete, sender=PublicationUpVote)
def post_delete_pub_up_vote(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)


@receiver(post_delete, sender=PublicationDownVote)
def post_delete_pub_down_vote(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_dislikes(instance)


@receiver(post_delete, sender=PublicationShare)
def post_delete_pub_share(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)


@receiver(post_save, sender=PublicationBookmark)
def post_delete_pub_bookmark(sender, instance, **kwargs):
    decrease_popularity(instance)
    decrease_supports(instance)


@receiver(post_save, sender=HidePublication)
def post_delete_pub_hide(sender, instance, **kwargs):
    decrease_dislikes(instance)
