from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

from helpers.base_classes import Mains, check_assignment, models


class Block(Mains):
    profile = models.ForeignKey(
        "account.Profile",
        null=True,
        on_delete=models.CASCADE,
        related_name="blocks",
        editable=False,
    )
    community = models.ForeignKey(
        "community.Community",
        related_name="blocks",
        on_delete=models.CASCADE,
        null=True,
        editable=False,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_blocks",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        check_assignment(self, ["profile", "community"])
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["profile", "created_by"],
                condition=models.Q(profile__isnull=False),
                name="unique_profile_block",
            ),
            UniqueConstraint(
                fields=["community", "created_by"],
                condition=models.Q(community__isnull=False),
                name="unique_community_block",
            ),
        ]
