from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from helpers.notify import notify_author
from helpers.update_reactions import add_dislikes, decrease_dislikes
from report.models import Report


@receiver(post_save, sender=Report)
def post_save_report(sender, instance, created, **kwargs):
    if created:
        add_dislikes(instance)
        reported_instance = (
            instance.user
            or instance.publication
            or instance.comment
            or instance.community
            or instance.share
        )
        notify_author(reported_instance, instance, "reported")
        # notify_mods()
        # notify_super_users()


@receiver(post_delete, sender=Report)
def post_delete_report(sender, instance, **kwargs):
    decrease_dislikes(instance)
