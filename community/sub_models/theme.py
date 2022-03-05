from django.contrib.auth import get_user_model
from django.db import models

from choices import COLOR_CHOICES


class Theme(models.Model):
    color = models.CharField(choices=COLOR_CHOICES, max_length=32, default="primary")
    subscriber_nickname = models.CharField(max_length=64, default="Subscribers")
    state_after_subscription = models.CharField(max_length=64, default="Awesome")
    community = models.OneToOneField(
        "Community",
        editable=False,
        on_delete=models.CASCADE,
        related_name="theme",
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_community_themes",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
