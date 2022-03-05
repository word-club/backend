from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.constraints import UniqueConstraint

from choices import REPORT_STATES
from comment.models import Comment
from community.models import Community
from publication.models import Publication
from share.models import Share


class Report(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reports",
        editable=False,
        null=True,
    )
    publication = models.ForeignKey(
        Publication,
        related_name="reports",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    comment = models.ForeignKey(
        Comment,
        related_name="reports",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    community = models.ForeignKey(
        Community,
        related_name="reports",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    share = models.ForeignKey(
        Share,
        related_name="reports",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_reports",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(default="pending", max_length=8, choices=REPORT_STATES)

    resolve_text = models.TextField(null=True, editable=False)
    resolved_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="resolved_reports",
        editable=False,
        null=True,
    )
    resolved_at = models.DateTimeField(null=True, editable=False)

    def is_resolved(self):
        return self.status == "resolved"

    def is_ignored(self):
        return self.status == "ignored"

    def is_pending(self):
        return self.status == "pending"

    def save(self, *args, **kwargs):
        check = 0
        if self.user:
            check += 1
        if self.publication:
            check += 1
        if self.comment:
            check += 1
        if self.community:
            check += 1
        if self.share:
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
                fields=["user", "created_by"],
                condition=models.Q(user__isnull=False),
                name="unique_user_report",
            ),
            UniqueConstraint(
                fields=["publication", "created_by"],
                condition=models.Q(publication__isnull=False),
                name="unique_publication_report",
            ),
            UniqueConstraint(
                fields=["comment", "created_by"],
                condition=models.Q(comment__isnull=False),
                name="unique_comment_report",
            ),
            UniqueConstraint(
                fields=["community", "created_by"],
                condition=models.Q(community__isnull=False),
                name="unique_community_report",
            ),
            UniqueConstraint(
                fields=["share", "created_by"],
                condition=models.Q(share__isnull=False),
                name="unique_share_report",
            ),
        ]
