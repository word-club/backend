from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models


class Notification(models.Model):
    is_global = models.BooleanField(default=False)

    subject = models.CharField(max_length=64)
    description = models.CharField(max_length=255, blank=True, null=True)

    publication = models.ForeignKey(
        "publication.Publication",
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    community = models.ForeignKey(
        "community.Community",
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    comment = models.ForeignKey(
        "comment.Comment",
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    vote = models.ForeignKey(
        "vote.Vote",
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    share = models.ForeignKey(
        "share.Share",
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    subscription = models.ForeignKey(
        "community.Subscription",
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    bookmark = models.ForeignKey(
        "bookmark.Bookmark",
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    follow = models.ForeignKey(
        "account.FollowUser",
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    report = models.ForeignKey(
        "report.Report",
        null=True,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        check = 0
        if self.publication:
            check += 1
        if self.community:
            check += 1
        if self.comment:
            check += 1
        if self.vote:
            check += 1
        if self.share:
            check += 1
        if self.subscription:
            check += 1
        if self.bookmark:
            check += 1
        if self.follow:
            check += 1
        if self.report:
            check += 1
        if check == 0:
            raise ValidationError({"detail": "One of the key field must be specified"})
        if check > 1:
            raise ValidationError({"detail": "Only one key field can be submitted"})
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]


class NotificationTo(models.Model):
    seen = models.BooleanField(default=False, editable=False)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="received_notifications",
    )
    notification = models.ForeignKey(
        "Notification",
        on_delete=models.CASCADE,
        related_name="receivers",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
