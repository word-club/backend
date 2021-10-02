import uuid

from django.contrib.auth import get_user_model
from django.db import models

from comment.models import Comment
from community.models import Community
from publication.models import Publication


class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    is_global = models.BooleanField(default=False)

    subject = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class NotificationTo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
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
        editable=False
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class PublicationNotification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    timestamp = models.DateTimeField(auto_now=True)
    notification = models.ForeignKey(
        "Notification",
        on_delete=models.CASCADE,
        related_name="publications",
        editable=False
    )

    class Meta:
        ordering = ["-timestamp"]


class CommunityNotification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    timestamp = models.DateTimeField(auto_now=True)
    notification = models.ForeignKey(
        "Notification",
        on_delete=models.CASCADE,
        related_name="communities",
        editable=False
    )

    class Meta:
        ordering = ["-timestamp"]


class CommentNotification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    notification = models.ForeignKey(
        "Notification",
        on_delete=models.CASCADE,
        related_name="comments",
        editable=False
    )

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
