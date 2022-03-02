from django.db import models
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from comment.models import Comment
from publication.models import Publication


class Vote(models.Model):
    publication = models.ForeignKey(
        Publication,
        related_name="votes",
        on_delete=models.CASCADE,
        editable=False,
        null=True
    )
    comment = models.ForeignKey(
        Comment,
        related_name="votes",
        on_delete=models.CASCADE,
        editable=False,
        null=True
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="votes",
        editable=False,
    )

    up = models.BooleanField(default=False, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        check = 0
        if self.publication:
            check += 1
        if self.comment:
            check += 1
        if check > 1:
            raise ValidationError({
                "detail": "Only one key field is allowed."
            })

    class Meta:
        ordering = ["-timestamp"]
        constraints = [
            UniqueConstraint(
                fields=['publication', 'created_by'],
                condition=models.Q(publication__isnull=False),
                name='unique_report_target'
            ),
            UniqueConstraint(
                fields=['comment', 'created_by'],
                condition=models.Q(comment__isnull=False),
                name='unique_report_target'
            ),
        ]