import uuid

from django.contrib.auth import get_user_model
from django.db import models


class Hashtag(models.Model):

    tag = models.CharField(max_length=64, unique=True)

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        related_name="created_hashtags",
    )
    timestamp = models.DateTimeField(auto_now_add=True)
