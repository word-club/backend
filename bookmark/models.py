from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model

from comment.models import Comment
from publication.models import Publication


class Bookmark(models.Model):
    comment = models.ForeignKey(
        Comment,
        related_name="bookmarks",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    publication = models.ForeignKey(
        Publication,
        related_name="bookmarks",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="bookmarks",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        check = 0
        if self.publication:
            check += 1
        if self.comment:
            check += 1
        if check > 1:
            raise Exception("Only one key field is allowed.")
        super().save(*args, **kwargs)

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
