from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from comment.models import Comment
from community.models import Community
from publication.models import Publication


class Hide(models.Model):
    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name="hidden",
        editable=False,
        null=True,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="hidden",
        editable=False,
        null=True,
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="hidden",
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_hides",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        check = 0
        if self.publication:
            check += 1
        if self.community:
            check += 1
        if self.comment:
            check += 1
        if check == 0:
            raise ValidationError({"detail": "One of the key field must be specified"})
        if check > 1:
            raise ValidationError({"detail": "Only one key field can be submitted"})
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["publication", "created_by"],
                condition=models.Q(publication__isnull=False),
                name="unique_publication_user_hide",
            ),
            UniqueConstraint(
                fields=["community", "created_by"],
                condition=models.Q(community__isnull=False),
                name="unique_community_user_hide",
            ),
            UniqueConstraint(
                fields=["comment", "created_by"],
                condition=models.Q(comment__isnull=False),
                name="unique_comment_user_hide",
            ),
        ]
