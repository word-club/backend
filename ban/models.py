from django.db import models
from django.contrib.auth import get_user_model
from choices import BAN_ITEM_MODEL_CHOICES, BAN_ITEM_APP_LABEL_CHOICES


class Ban(models.Model):
    ban_reason = models.TextField()

    ban_item_id = models.PositiveBigIntegerField()
    ban_item_app_label = models.CharField(choices=BAN_ITEM_APP_LABEL_CHOICES, max_length=32)
    ban_item_model = models.CharField(choices=BAN_ITEM_MODEL_CHOICES, max_length=32)

    banned_at = models.DateTimeField(null=True, editable=False)
    banned_by = models.ForeignKey(
        get_user_model(), null=True, editable=False, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["-banned_at"]
        unique_together = [["ban_item_app_label", "ban_item_id", "ban_item_model"]]

    def __str__(self):
        return f"{self.ban_item_model} {self.ban_item_id}"
