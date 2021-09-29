from django.db.models.signals import post_save
from django.dispatch import receiver

from community.models import Community, CommunityAdmin


@receiver(post_save, sender=Community)
def set_creator_as_community_admin(sender, instance, created, **kwargs):
    if created:
        community_writer = instance.created_by
        CommunityAdmin.objects.create(
            user=community_writer, created_by=community_writer, community=instance
        )
