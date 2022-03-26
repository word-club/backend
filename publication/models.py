from django.contrib.auth import get_user_model
from django.db import models

from choices import PUBLICATION_TYPE_CHOICES
from community.models import Community
from hashtag.models import Hashtag


class Publication(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField(null=True, blank=True)

    is_published = models.BooleanField(default=False, editable=False)
    published_at = models.DateTimeField(null=True, editable=False)

    is_pinned = models.BooleanField(default=False, editable=False)
    pinned_at = models.DateTimeField(null=True, editable=False)
    pinned_by = models.ForeignKey(
        get_user_model(), null=True, editable=False, on_delete=models.SET_NULL
    )

    views = models.PositiveBigIntegerField(default=0, editable=False)

    type = models.CharField(max_length=32, choices=PUBLICATION_TYPE_CHOICES, default="editor")

    tags = models.ManyToManyField(
        Hashtag,
        blank=True,
        related_name="publications",
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
        related_name="my_publications",
        editable=False,
    )

    popularity = models.PositiveBigIntegerField(default=0, editable=False)
    dislikes = models.PositiveBigIntegerField(default=0, editable=False)
    supports = models.PositiveBigIntegerField(default=0, editable=False)
    discussions = models.PositiveBigIntegerField(default=0, editable=False)

    # TODO: implement ban one to one relation
    # is_banned = models.BooleanField(default=False, editable=False)
    # banned_at = models.DateTimeField(null=True, editable=False)
    # banned_by = models.ForeignKey(
    #     get_user_model(), null=True, editable=False, on_delete=models.SET_NULL
    # )
    # ban_reason_title = models.CharField(max_length=128, null=True, editable=False)
    # ban_reason_content = models.TextField(null=True, blank=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def is_draft(self):
        return not self.is_published


class RecentPublication(models.Model):
    publication = models.ForeignKey(
        Publication, on_delete=models.CASCADE, related_name="recent_viewers"
    )
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="recent_publications"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["publication", "created_by"]]
