from django.contrib.auth import get_user_model
from django.db import models

from community.models import Community
from publication.models import Publication


class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    for_everyone = models.BooleanField(default=False)

    subject = models.CharField(max_length=64)
    description = models.CharField(max_length=255)

    target = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="notifications"
    )

    user_involved = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="involvements"
    )

    publication_involved = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name = "involvements"
    )

    community_involved = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="involvements"
    )

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
