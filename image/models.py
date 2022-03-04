from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from helpers.upload_path import upload_image_to
from publication.models import Publication
from comment.models import Comment
from backend.settings import ALLOWED_IMAGES_EXTENSIONS


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
        check = 0
        if self.image_url:
            check += 1
        if self.image:
            check += 1
        if check == 0:
            raise ValidationError(
                {"detail": "One of the image field must be specified"}
            )
        if check > 1:
            raise ValidationError({"detail": "Only one image field can be submitted"})
        check = 0
        if self.publication:
            check += 1
        if self.comment:
            check += 1
        if check == 0:
            raise ValidationError({"detail": "One of the key field must be specified"})
        if check > 1:
            raise ValidationError({"detail": "Only one key field can be submitted"})
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)
