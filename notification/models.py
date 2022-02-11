from django.contrib.auth import get_user_model
from django.db import models

from comment.models import Comment
from community.models import Community, CommunitySubscription
from publication.models import Publication


class Notification(models.Model):
    is_global = models.BooleanField(default=False)

    subject = models.CharField(max_length=64)
    description = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    publication = models.ForeignKey(
        Publication,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    community = models.ForeignKey(
        Community,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    comment = models.ForeignKey(
        Comment,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    # upvote
    # down vote
    # share
    # bookmark
    # follow
    subscription = models.ForeignKey(
        CommunitySubscription,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    # report

    class Meta:
        ordering = ["-timestamp"]


class NotificationTo(models.Model):
    seen = models.BooleanField(default=False, editable=False)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="received_notifications",
    )
    notification = models.ForeignKey(
        "Notification",
        on_delete=models.CASCADE,
        related_name="receivers",
        editable=False,
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
