import os
import random
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import ALLOWED_IMAGES_EXTENSIONS
from publication.models import Publication


def upload_comment_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"comments/{instance.comment.pk}/{filename}"


def upload_reply_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"replies/{instance.reply.pk}/{filename}"


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    comment = models.TextField()
    publication = models.ForeignKey(
        Publication,
        related_name="comments",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="comments",
        editable=False,
    )

    is_pinned = models.BooleanField(default=False, editable=False)

    timestamp = models.DateTimeField(auto_now=True)

    reply = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, blank=True, related_name="replies"
    )

    class Meta:
        ordering = ["-timestamp"]


class CommentImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    image = models.ImageField(
        upload_to=upload_comment_image_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    comment = models.ForeignKey(
        "Comment",
        related_name="images",
        on_delete=models.CASCADE,
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)


class CommentImageUrl(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    url = models.URLField()
    comment = models.ForeignKey(
        "Comment",
        related_name="image_urls",
        on_delete=models.CASCADE,
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class CommentLink(models.Model):
    link = models.URLField()
    title = models.CharField(max_length=512, editable=False, null=True)
    image = models.URLField(editable=False, null=True)
    description = models.TextField(editable=False, null=True)
    comment = models.OneToOneField(
        "Comment", on_delete=models.CASCADE, related_name="link", editable=False
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["comment", "link"]]


class CommentUpVote(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    comment = models.ForeignKey(
        "Comment",
        related_name="up_votes",
        on_delete=models.CASCADE,
        editable=False,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="up_voted_comments",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["created_by", "comment"]]


class CommentDownVote(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    comment = models.ForeignKey(
        "Comment",
        related_name="down_votes",
        on_delete=models.CASCADE,
        editable=False,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="down_voted_comments",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["created_by", "comment"]]


class ReportComment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    reason = models.TextField()
    comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="reports", editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reported_comments",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class HideComment(models.Model):
    comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="hides", editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="hidden_comments",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["comment", "created_by"]]


class CommentShare(models.Model):
    title = models.CharField(max_length=128)
    comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="shares", editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="shared_comments",
        editable=False,
    )
    tags = models.CharField(max_length=16, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["comment", "created_by"]]


class CommentBookmark(models.Model):
    comment = models.ForeignKey(
        "Comment",
        related_name="bookmarks",
        on_delete=models.CASCADE,
        editable=False,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="saved_comments",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["comment", "created_by"]]
