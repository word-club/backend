from django.db.models.signals import post_save
from django.dispatch import receiver

from helpers.update_reactions import notify_author
from report.models import Report


@receiver(post_save, sender=Report)
def post_save_report(sender, instance, created, **kwargs):
    if created:
        reported_instance = (
            instance.user
            or instance.publication
            or instance.comment
            or instance.community
            or instance.share
        )
        notify_author(reported_instance, instance, "report", "reported_by")
