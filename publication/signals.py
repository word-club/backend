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
        publication = instance.publication
        if publication.popularity > 0:
            publication.popularity += 1
            publication.save()
        if publication.created_by.profile.popularity > 0:
            publication.created_by.profile.popularity += 1
            publication.created_by.profile.save()
        if publication.community and publication.community.popularity > 0:
            publication.community.popularity += 1
            publication.community.save()


def add_dislikes(instance, created):
    if created:
        publication = instance.publication
        if publication.dislikes > 0:
            publication.dislikes += 1
            publication.save()
        if publication.created_by.profile.dislikes > 0:
            publication.created_by.profile.dislikes += 1
            publication.created_by.profile.save()
        if publication.community and publication.community.dislikes > 0:
            publication.community.dislikes += 1
            publication.community.save()


def add_supports(instance, created):
    if created:
        publication = instance.publication
        if publication.supports > 0:
            publication.supports += 1
            publication.save()
        if publication.created_by.profile.supports > 0:
            publication.created_by.profile.supports += 1
            publication.created_by.profile.save()
        if publication.community and publication.community.supports > 0:
            publication.community.supports += 1
            publication.community.save()


def decrease_popularity(instance):
    publication = instance.publication
    if publication.popularity > 0:
        publication.popularity -= 1
        publication.save()
    if publication.created_by.profile.popularity > 0:
        publication.created_by.profile.popularity -= 1
        publication.created_by.profile.save()
    if publication.community and publication.community.popularity > 0:
        publication.community.popularity -= 1
        publication.community.save()


def decrease_dislikes(instance):
    publication = instance.publication
    if publication.dislikes > 0:
        publication.dislikes -= 1
        publication.save()
    if publication.created_by.profile.dislikes > 0:
        publication.created_by.profile.dislikes -= 1
        publication.created_by.profile.save()
    if publication.community and publication.community.dislikes > 0:
        publication.community.dislikes -= 1
        publication.community.save()


def decrease_supports(instance):
    publication = instance.publication
    if publication.supports > 0:
        publication.supports -= 1
        publication.save()
    if publication.created_by.profile.supports > 0:
        publication.created_by.profile.supports -= 1
        publication.created_by.profile.save()
    if publication.community and publication.community.supports > 0:
        publication.community.supports -= 1
        publication.community.save()


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
