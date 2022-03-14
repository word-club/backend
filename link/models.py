from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

from comment.models import Comment
from publication.models import Publication


class Link(models.Model):
    link = models.URLField()
    image = models.URLField(editable=False, null=True)
    description = models.TextField(editable=False, null=True)
    title = models.CharField(max_length=512, editable=False, null=True)
    publication = models.OneToOneField(
        Publication,
        on_delete=models.CASCADE,
        related_name="links",
        editable=False,
        null=True,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="links",
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_links",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        check = 0
        if self.publication:
            if self.publication.type != 'link':
                raise ValidationError({"detail": "Publication is not a link"})
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
                fields=["publication", "link"],
                condition=models.Q(publication__isnull=False),
                name="unique_publication_link",
            ),
            UniqueConstraint(
                fields=["comment", "link"],
                condition=models.Q(comment__isnull=False),
                name="unique_comment_link",
            ),
        ]
