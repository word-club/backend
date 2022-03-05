from django.contrib.auth import get_user_model
from django.db import models


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_subscriptions",
        editable=False,
    )
    community = models.ForeignKey(
        "Community",
        on_delete=models.CASCADE,
        related_name="subscriptions",
        editable=False,
    )

    disable_notification = models.BooleanField(default=False, editable=False)

    is_approved = models.BooleanField(default=False, editable=False)
    approved_at = models.DateTimeField(null=True, editable=False)

    is_banned = models.BooleanField(default=False, editable=False)
    ban_reason = models.TextField(null=True, editable=False)
    banned_at = models.DateTimeField(null=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["subscriber", "community"]]
