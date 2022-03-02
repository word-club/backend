from django.db import models
from django.contrib.auth import get_user_model

from comment.models import Comment
from publication.models import Publication


class Share(models.Model):
    publication = models.ForeignKey(
        Publication,
        related_name="shares",
        on_delete=models.CASCADE,
        editable=False,
        null=True
    )
    comment = models.ForeignKey(
        Comment,
        related_name="shares",
        on_delete=models.CASCADE,
        editable=False,
        null=True
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="shares",
        editable=False,
    )

    title = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [
            ["comment", "created_by"],
            ["publication", "created_by"]
        ]
