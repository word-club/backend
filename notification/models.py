import uuid

from django.contrib.auth import get_user_model
from django.db import models

from comment.models import Comment
from community.models import Community
from publication.models import Publication


class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    is_read = models.BooleanField(default=False)
    for_everyone = models.BooleanField(default=False)

    subject = models.CharField(max_length=64)
    description = models.CharField(max_length=255)

    target = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )

    user_involved = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="involvements",
    )

    publication_involved = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="involvements",
    )

    community_involved = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="involvements",
    )

    comment_involved = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="involvements",
    )

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
