from django.contrib.auth import get_user_model

from ban.models import Ban
from choices import PUBLICATION_TYPE_CHOICES
from community.models import Community
from hashtag.models import Hashtag
from helpers.base_classes import Reactions, models


class Publication(Reactions):
    title = models.CharField(max_length=128)
    content = models.TextField(null=True, blank=True)

    is_published = models.BooleanField(default=False, editable=False)
    published_at = models.DateTimeField(null=True, editable=False)

    # TODO: implement pub access type (public, private, community)
    # TODO: implement eighteen plus (18+)

    # TODO: implement pin from different app
    is_pinned = models.BooleanField(default=False, editable=False)
    pinned_at = models.DateTimeField(null=True, editable=False)
    pinned_by = models.ForeignKey(
        get_user_model(), null=True, editable=False, on_delete=models.SET_NULL
    )

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def is_draft(self):
        return not self.is_published

    @property
    def is_banned(self):
        try:
            return Ban.objects.get(
                ban_item_id=self.pk,
                ban_item_app_label="publication",
                ban_item_model="publication",
            )
        except Ban.DoesNotExist:
            return False


class RecentPublication(models.Model):
    """
    This model is used to keep track of the recent publications viewed by a user.
    """

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
