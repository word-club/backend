import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from community.models import Community


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
        check = 0
        if self.community:
            check += 1
        if self.user:
            check += 1
        if check == 0:
            raise ValidationError({"detail": "One of the key field must be specified"})
        if check > 1:
            raise ValidationError({"detail": "Only one key field can be submitted"})
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

