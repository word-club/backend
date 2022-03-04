from django.contrib.auth import get_user_model
from django.db import models

from administration.models import Administration
from choices import PUBLICATION_TYPE_CHOICES
from community.models import Community
from hashtag.models import Hashtag


class Publication(models.Model):

    title = models.CharField(max_length=128)
    content = models.TextField(null=True, blank=True)

    is_published = models.BooleanField(default=False, editable=False)
    published_at = models.DateTimeField(null=True, editable=False)

    is_pinned = models.BooleanField(default=False, editable=False)

    views = models.PositiveBigIntegerField(default=0, editable=False)

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

    def is_draft(self):
        return not self.is_published


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
