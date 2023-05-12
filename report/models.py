from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from choices import REPORT_STATES
from helpers.base_classes import (
    Mains,
    get_constraints,
    UniqueConstraint,
)
from helpers.helper import check_for_mains_unique_model_assignment
from share.models import Share


class Report(Mains):
    title = models.CharField(max_length=256)
    content = models.TextField()
    share = models.ForeignKey(
        Share,
        related_name="reports",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )

    status = models.CharField(default="pending", max_length=8, choices=REPORT_STATES)

    resolve_text = models.TextField(null=True, editable=False)
    resolved_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="resolved_reports",
        editable=False,
        null=True,
    )
    resolved_at = models.DateTimeField(null=True, editable=False)

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_reports",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_resolved(self):
        return self.status == "resolved"

    def is_ignored(self):
        return self.status == "ignored"

    def is_pending(self):
        return self.status == "pending"

    def save(self, *args, **kwargs):
        check_for_mains_unique_model_assignment(self, ["share"])
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        constraints = get_constraints("report") + [
            UniqueConstraint(
                fields=["share", "created_by"],
                condition=models.Q(share__isnull=True),
                name="unique_share_user_report",
            )
        ]
