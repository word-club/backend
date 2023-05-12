from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings.base import ALLOWED_IMAGES_EXTENSIONS
from comment.models import Comment
from helpers.helper import check_if_a_key_field_is_present
from helpers.upload_path import upload_image_to
from publication.models import Publication


class Image(models.Model):
    image_url = models.URLField(null=True)
    image = models.ImageField(
        upload_to=upload_image_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
        null=True,
    )
    publication = models.ForeignKey(
        Publication,
        related_name="images",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    comment = models.ForeignKey(
        Comment,
        related_name="images",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        related_name="images",
        on_delete=models.CASCADE,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.id:
            check_if_a_key_field_is_present(self, "image_url", "image")
            check_if_a_key_field_is_present(self, "publication", "comment")
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)
