from django.db import models
from django.contrib.auth import get_user_model

from choices import MOD_CHOICES


class Moderator(models.Model):
    role = models.CharField(max_length=3, choices=MOD_CHOICES)
    is_accepted = models.BooleanField(default=False, editable=False)
    accepted_at = models.DateTimeField(null=True, editable=False)
    community = models.ForeignKey(
        "Community",
        on_delete=models.CASCADE,
        related_name="moderators",
        editable=False
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="managed_communities",
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="created_community_moderators",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["user", "community", "role"]]
