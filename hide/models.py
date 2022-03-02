from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from comment.models import Comment
from publication.models import Publication


class Hide(models.Model):
    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name="hidden",
        editable=False
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="hidden",
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="hidden",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now=True)

    def clean(self):
        check = 0
        if self.publication:
            check += 1
        if self.comment:
            check += 1
        if check != 0 and check > 1:
            raise ValidationError({'detail': 'Only one key field can be submitted'})

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=['publication', 'created_by'],
                condition=models.Q(publication__isnull=False),
                name='unique_publication_user_bookmark'
            ),
            UniqueConstraint(
                fields=['comment', 'created_by'],
                condition=models.Q(comment__isnull=False),
                name='unique_comment_user_bookmark'
            ),
        ]


