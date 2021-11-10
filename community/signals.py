from django.db.models.signals import post_save
from django.dispatch import receiver

from choices import PROGRESS_STATES
from community.models import (
    Community,
    CommunityAdmin,
    CommunityCreateProgress,
    CommunitySubscription,
    CommunityTheme,
)


def set_admin_and_subscriber(instance, writer):
    CommunityAdmin.objects.create(user=writer, created_by=writer, community=instance)
    CommunitySubscription.objects.create(subscriber=writer, community=instance)


def init_progress_states(instance):
    for (key, value) in PROGRESS_STATES:
        CommunityCreateProgress.objects.create(community=instance, state=key)


def init_theme(instance, writer):
    CommunityTheme.objects.create(community=instance, created_by=writer)


@receiver(post_save, sender=Community)
def setup_post_community_actions(sender, instance, created, **kwargs):
    if created:
        writer = instance.created_by
        set_admin_and_subscriber(instance, writer)
        init_progress_states(instance)
        init_theme(instance, writer)
