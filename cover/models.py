from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from account.models import Profile
from backend.settings.base import ALLOWED_IMAGES_EXTENSIONS
from community.models import Community
from helpers.upload_path import upload_cover_to


class Cover(models.Model):
    image = models.ImageField(
        upload_to=upload_cover_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="covers",
        null=True,
        editable=False,
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="covers",
        null=True,
        editable=False,
    )

    is_active = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        get_user_model(),
        related_name="my_covers",
        on_delete=models.CASCADE,
        editable=False,
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        check = 0
        if self.community:
            check += 1
        if self.profile:
            check += 1
        if check == 0:
            raise ValidationError({"detail": "One of the key field must be specified"})
        if check > 1:
            raise ValidationError({"detail": "Only one key field can be submitted"})

        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)
