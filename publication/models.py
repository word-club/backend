import os
import random
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import ALLOWED_IMAGES_EXTENSIONS
from hashtag.models import HashTag


def upload_publication_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"publications/{instance.publication.pk}/images/{filename}"


class Publication(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    views = models.PositiveBigIntegerField(default=0)
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    writer = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="publications"
    )

    is_published = models.BooleanField(default=False, editable=False)
    published_at = models.DateTimeField(null=True, blank=True)

    is_pinned = models.BooleanField(default=False, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class PublicationHashtag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    tag = models.ForeignKey(
        HashTag, related_name="publications", on_delete=models.CASCADE
    )
    publication = models.ForeignKey(
        "Publication", related_name="hashtags", on_delete=models.CASCADE, editable=False
    )


class PublicationImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    image = models.ImageField(
        upload_to=upload_publication_image_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    publication = models.ForeignKey(
        "Publication", related_name="images", on_delete=models.CASCADE
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
        "Publication", related_name="image_urls", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class Bookmark(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    is_bookmarked = models.BooleanField(default=True)

    publication = models.ForeignKey(
        "Publication", related_name="bookmarks", on_delete=models.CASCADE
    )
    writer = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="bookmarks"
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class UpVote(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    up_vote = models.BooleanField(default=True)

    publication = models.ForeignKey(
        "Publication", related_name="up_votes", on_delete=models.CASCADE
    )
    writer = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="up_voted_publications"
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class DownVotes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    down_vote = models.BooleanField(default=True)

    publication = models.ForeignKey(
        "Publication", related_name="down_votes", on_delete=models.CASCADE
    )
    writer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="down_voted_publications",
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class ReportPublication(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    reason = models.TextField()

    publication = models.ForeignKey(
        "Publication", on_delete=models.CASCADE, related_name="reports"
    )
    writer = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reported_publications"
    )
    timestamp = models.DateTimeField(auto_now=True)
