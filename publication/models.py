import os
import random

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import ALLOWED_IMAGES_EXTENSIONS
from choices import PUBLICATION_TYPE_CHOICES
from community.models import Community


def upload_publication_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"publications/{instance.publication.pk}/images/{filename}"


class Publication(models.Model):

    title = models.CharField(max_length=128)
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
    tags = models.CharField(max_length=16, null=True, blank=True)

    type = models.CharField(
        max_length=32, choices=PUBLICATION_TYPE_CHOICES, default="editor"
    )

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


class PublicationImage(models.Model):

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
        related_name="bookmark",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]


class PublicationUpVote(models.Model):

    publication = models.ForeignKey(
        "Publication", related_name="up_votes", on_delete=models.CASCADE, editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="up_vote",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]


class PublicationDownVote(models.Model):

    publication = models.ForeignKey(
        "Publication",
        related_name="down_votes",
        on_delete=models.CASCADE,
        editable=False,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="down_vote",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]


class HidePublication(models.Model):

    publication = models.ForeignKey(
        "Publication",
        on_delete=models.CASCADE,
        related_name="hides",
        editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="hidden_status",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]


class ReportPublication(models.Model):

    reason = models.TextField()

    publication = models.ForeignKey(
        "Publication", on_delete=models.CASCADE, related_name="reports", editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="report",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]


class PublicationLink(models.Model):
    link = models.URLField()
    title = models.CharField(max_length=512, editable=False, null=True)
    image = models.URLField(editable=False, null=True)
    description = models.TextField(editable=False, null=True)
    publication = models.OneToOneField(
        "Publication", on_delete=models.CASCADE, related_name="link", editable=False
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "link"]]


class PublicationShare(models.Model):
    title = models.CharField(max_length=128)
    publication = models.ForeignKey(
        "Publication",
        on_delete=models.CASCADE,
        related_name="shares",
        editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="share",
        editable=False,
    )
    tags = models.CharField(max_length=16, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]
