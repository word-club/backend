from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

from helpers.base_classes import check_assignment, models


class Vote(models.Model):
    publication = models.ForeignKey(
        "publication.Publication",
        related_name="votes",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    comment = models.ForeignKey(
        "comment.Comment",
        related_name="votes",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_votes",
        editable=False,
    )

    up = models.BooleanField(default=False, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        check_assignment(self, ["publication", "comment"])
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["up", "publication", "created_by"],
                condition=models.Q(publication__isnull=False),
                name="unique_publication_vote",
            ),
            UniqueConstraint(
                fields=["up", "comment", "created_by"],
                condition=models.Q(comment__isnull=False),
                name="unique_comment_vote",
            ),
        ]
