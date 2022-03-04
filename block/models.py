from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError

from community.models import Community


class Block(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="blocks",
        editable=False,
    )
    community = models.ForeignKey(
        Community,
        related_name="blocks",
        on_delete=models.CASCADE,
        editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_blocks",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        check = 0
        if self.user:
            check += 1
        if self.community:
            check += 1
        if check == 0:
            raise ValidationError({"detail": "One of the key field must be specified"})
        if check > 1:
            raise ValidationError({"detail": "Only one key field can be submitted"})
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["user", "created_by"],
                condition=models.Q(user__isnull=False),
                name="unique_user_block",
            ),
            UniqueConstraint(
                fields=["community", "created_by"],
                condition=models.Q(community__isnull=False),
                name="unique_community_block",
            ),
        ]
