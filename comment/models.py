from django.contrib.auth import get_user_model

from helpers.base_classes import Reactions, models
from publication.models import Publication


class Comment(Reactions):
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
        related_name="my_comments",
        editable=False,
    )

    is_pinned = models.BooleanField(default=False, editable=False)
    pinned_at = models.DateTimeField(null=True, editable=False)
    pinned_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_pinned_comments",
        editable=False,
        null=True,
    )

    reply = models.ForeignKey("self", null=True, on_delete=models.CASCADE, related_name="replies")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.comment
