import uuid

from django.contrib.auth import get_user_model
from django.db import models


class HashTag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    tag = models.CharField(max_length=64)

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        related_name="created_hashtags",
    )
    timestamp = models.DateTimeField(auto_now_add=True)
