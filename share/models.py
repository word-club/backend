from django.db import models
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from comment.models import Comment
from community.models import Community
from publication.models import Publication


class Share(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="shares",
        editable=False,
        null=True,
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="shares",
        editable=False,
        null=True,
    )
    publication = models.ForeignKey(
        Publication,
        related_name="shares",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    comment = models.ForeignKey(
        Comment,
        related_name="shares",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_shares",
        editable=False,
    )

    title = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        check = 0
        if self.user:
            check += 1
        if self.community:
            check += 1
        if self.publication:
            check += 1
        if self.comment:
            check += 1
        if check == 0:
            raise ValidationError({"detail": "One of the key field must be specified"})
        if check > 1:
            raise ValidationError({"detail": "Only one key field can be submitted"})

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["publication", "created_by"],
                condition=models.Q(publication__isnull=False),
                name="unique_publication_share",
            ),
            UniqueConstraint(
                fields=["comment", "created_by"],
                condition=models.Q(comment__isnull=False),
                name="unique_comment_share",
            ),
        ]
