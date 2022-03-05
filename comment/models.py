from django.contrib.auth import get_user_model
from django.db import models

from administration.models import Administration
from publication.models import Publication


class Comment(models.Model):
    comment = models.TextField()
    publication = models.ForeignKey(
        Publication,
        related_name="comments",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="comments",
        editable=False,
    )

    popularity = models.PositiveBigIntegerField(default=0, editable=False)
    dislikes = models.PositiveBigIntegerField(default=0, editable=False)
    supports = models.PositiveBigIntegerField(default=0, editable=False)
    discussions = models.PositiveBigIntegerField(default=0, editable=False)

    is_pinned = models.BooleanField(default=False, editable=False)
    pinned_at = models.DateTimeField(null=True, editable=False)
    pinned_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_pinned_comments",
        editable=False,
        null=True,
    )

    reply = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, related_name="replies"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
