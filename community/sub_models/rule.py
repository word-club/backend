from django.contrib.auth import get_user_model
from django.db import models


class Rule(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="rules", editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_community_rules",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        unique_together = [["community", "title"]]
