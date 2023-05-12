import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from community.models import Community
from helpers.helper import check_if_a_key_field_is_present


class AuthorizationCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(
        get_user_model(),
        editable=False,
        on_delete=models.CASCADE,
        related_name="auth_code",
        null=True,
    )
    community = models.OneToOneField(
        Community,
        editable=False,
        on_delete=models.CASCADE,
        related_name="auth_code",
        null=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="created_auth_codes",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        check_if_a_key_field_is_present(self, "community", "user")
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]


class ResetPasswordCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reset_password_codes",
        unique=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="created_reset_codes",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
