from django.contrib.auth import get_user_model
from django.db import models


class Hashtag(models.Model):
    tag = models.CharField(max_length=64, unique=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        editable=False,
        related_name="my_hashtags",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
