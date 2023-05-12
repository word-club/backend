from django.contrib.auth import get_user_model
from django.db import models

from helpers.base_classes import Mains, get_constraints
from helpers.helper import check_for_mains_unique_model_assignment


class Hide(Mains):
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_hides",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        check_for_mains_unique_model_assignment(self)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        constraints = get_constraints("hide")
