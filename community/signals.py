from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from community.helper import notify_community
from community.models import Community, Moderator, Subscription, Theme


def set_writer_as_mod(instance, writer):
    Moderator.objects.create(
        user=writer,
        role="mod",
        created_by=writer,
        community=instance,
        is_accepted=True,
        accepted_at=timezone.now(),
    )


def init_writer_subscription(instance, writer):
    Subscription.objects.create(
        created_by=writer,
        community=instance,
        is_approved=True,
        approved_at=timezone.now(),
    )


def init_theme(instance, writer):
    Theme.objects.create(community=instance, created_by=writer)


@receiver(post_save, sender=Community)
def setup_post_community_actions(sender, instance, created, **kwargs):
    if created:
        writer = instance.created_by
        set_writer_as_mod(instance, writer)
        init_writer_subscription(instance, writer)
        init_theme(instance, writer)


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance, created, **kwargs):
    notify_community(instance, created)
