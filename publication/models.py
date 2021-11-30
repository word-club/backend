import os
import random

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from rest_framework.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from administration.models import Administration
from backend.settings import ALLOWED_IMAGES_EXTENSIONS
from choices import PUBLICATION_TYPE_CHOICES
from community.models import Community
from hashtag.models import Hashtag


def upload_publication_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"publications/{instance.publication.pk}/images/{filename}"


class Publication(models.Model):

    title = models.CharField(max_length=128)
    content = models.TextField(null=True, blank=True)

    is_published = models.BooleanField(default=False, editable=False)
    published_at = models.DateTimeField(null=True, editable=False)

    is_pinned = models.BooleanField(default=False, editable=False)

    view_count = models.PositiveBigIntegerField(default=0, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=16, null=True)

    type = models.CharField(
        max_length=32, choices=PUBLICATION_TYPE_CHOICES, default="editor"
    )

    community = models.ForeignKey(
        Community,
        null=True,
        on_delete=models.CASCADE,
        related_name="publications",
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="publications",
        editable=False,
    )

    popularity = models.PositiveBigIntegerField(default=0, editable=False)
    dislikes = models.PositiveBigIntegerField(default=0, editable=False)
    supports = models.PositiveBigIntegerField(default=0, editable=False)
    discussions = models.PositiveBigIntegerField(default=0, editable=False)

    class Meta:
        ordering = ["-timestamp"]

    def save(self, *args, **kwargs):
        if self.id:
            now = timezone.now()
            diff = now - self.created_at
            limit = Administration.objects.first()
            if diff.days > limit.publication_update_limit:
                raise ValidationError(
                    {
                        "detail": "Sorry, you cannot update the publication after {} days.".format(
                            limit.publication_update_limit
                        )
                    }
                )
        return super().save(*args, **kwargs)

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
        related_name="saved_publications",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
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
        related_name="up_voted_publications",
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
        related_name="down_voted_publications",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]


class HidePublication(models.Model):

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
        "Publication", on_delete=models.CASCADE, related_name="shares", editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="shared_publications",
        editable=False,
    )
    tags = models.CharField(max_length=16, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "created_by"]]


class PublicationHashtag(models.Model):
    hashtag = models.ForeignKey(
        Hashtag, on_delete=models.CASCADE, related_name="publications", editable=False
    )
    publication = models.ForeignKey(
        "Publication",
        on_delete=models.CASCADE,
        related_name="hashtags",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["publication", "hashtag"]]
