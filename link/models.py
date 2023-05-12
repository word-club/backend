from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

from comment.models import Comment
from helpers.helper import check_if_a_key_field_is_present
from publication.models import Publication


class Link(models.Model):
    title = models.CharField(max_length=512, editable=False, null=True)
    description = models.TextField(editable=False, null=True)

    link = models.URLField()

    image = models.URLField(editable=False, null=True)

    publication = models.OneToOneField(Publication, on_delete=models.CASCADE, related_name="links", editable=False, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="links", editable=False, null=True)

    created_by = models.ForeignKey( get_user_model(), on_delete=models.CASCADE, related_name="my_links", editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        check_if_a_key_field_is_present(self, "publication", "comment")
        if self.publication:
            if self.publication.type != "link":
                raise ValidationError({"detail": "Publication is not a link"})
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
