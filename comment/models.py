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
    return f"publications/{instance.comment.publication.pk}/comments/{instance.comment.pk}/{filename}"


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    comment = models.TextField()
    publication = models.ForeignKey(
        Publication, related_name="comments", on_delete=models.CASCADE
    )
    writer = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="comments"
    )
    reply_to = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class CommentImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    image = models.ImageField(
        upload_to=upload_comment_image_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    comment = models.ForeignKey(
        "Comment", related_name="images", on_delete=models.CASCADE
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
    publication = models.ForeignKey(
        "Comment", related_name="image_urls", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class CommentVideoUrl(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    url = models.URLField()
    publication = models.ForeignKey(
        "Comment", related_name="video_urls", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class UpVote(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    up_vote = models.BooleanField(default=True)

    publication = models.ForeignKey(
        "Comment", related_name="up_votes", on_delete=models.CASCADE
    )
    writer = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="up_voted_comments"
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class DownVotes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    down_vote = models.BooleanField(default=True)

    publication = models.ForeignKey(
        "Comment", related_name="down_votes", on_delete=models.CASCADE
    )
    writer = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="down_voted_comments"
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class ReportComment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    reason = models.TextField()
    comment = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="reports"
    )
    writer = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reported_comments"
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
