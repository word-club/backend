import os
import random
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import ALLOWED_IMAGES_EXTENSIONS
from community.models import Community
from hashtag.models import Hashtag


def upload_publication_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"publications/{instance.publication.pk}/images/{filename}"


class Publication(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="publications",
        editable=False,
    )

    is_published = models.BooleanField(default=False, editable=False)
    published_at = models.DateTimeField(null=True, blank=True, editable=False)

    is_pinned = models.BooleanField(default=False, editable=False)

    view_count = models.PositiveBigIntegerField(default=0, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

    community = models.ForeignKey(
        Community,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="publications",
    )

    class Meta:
        ordering = ["-timestamp"]

    def is_draft(self):
        return not self.is_published


class PublicationHashtag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    tag = models.ForeignKey(
        Hashtag, related_name="publications", on_delete=models.CASCADE
    )
    publication = models.ForeignKey(
        "Publication", related_name="hashtags", on_delete=models.CASCADE, editable=False
    )

    class Meta:
        unique_together = [["publication", "tag"]]


class PublicationImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    image = models.ImageField(
        upload_to=upload_publication_image_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    publication = models.ForeignKey(
        "Publication", related_name="images", on_delete=models.CASCADE, editable=False
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)


class PublicationImageUrl(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    image_url = models.URLField()
    publication = models.ForeignKey(
        "Publication",
        related_name="image_urls",
        on_delete=models.CASCADE,
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class PublicationBookmark(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    is_bookmarked = models.BooleanField(default=True, editable=False)

    publication = models.ForeignKey(
        "Publication",
        related_name="bookmarks",
        on_delete=models.CASCADE,
        editable=False,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="bookmarks",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]


class PublicationUpVote(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    publication = models.ForeignKey(
        "Publication", related_name="up_votes", on_delete=models.CASCADE, editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="up_voted_publications",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]


class PublicationDownVote(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    publication = models.ForeignKey(
        "Publication",
        related_name="down_votes",
        on_delete=models.CASCADE,
        editable=False,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="down_voted_publications",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]


class HidePublication(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    publication = models.ForeignKey(
        "Publication", on_delete=models.CASCADE, related_name="hides", editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="hidden_publications",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]


class ReportPublication(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    reason = models.TextField()

    publication = models.ForeignKey(
        "Publication", on_delete=models.CASCADE, related_name="reports", editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reported_publications",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]
