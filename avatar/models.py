from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from account.models import Profile
from backend.settings.base import ALLOWED_IMAGES_EXTENSIONS
from community.models import Community
from helpers.helper import check_if_a_key_field_is_present
from helpers.upload_path import upload_avatar_to


class Avatar(models.Model):
    image = models.ImageField(
        upload_to=upload_avatar_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="avatars",
        null=True,
        editable=False,
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="avatars",
        null=True,
        editable=False,
    )

    is_active = models.BooleanField(default=False, editable=False)

    created_by = models.ForeignKey(
        get_user_model(),
        related_name="my_avatars",
        on_delete=models.CASCADE,
        editable=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        check_if_a_key_field_is_present(self, "community", "profile")
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)
