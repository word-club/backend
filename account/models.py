import os
import random
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import ALLOWED_IMAGES_EXTENSIONS


def upload_profile_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"profile/{instance.profile.user.pk}/image/{filename}"


def upload_cover_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"profile/{instance.profile.user.pk}/cover/{filename}"


class Profile(models.Model):

    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, editable=False
    )
    bio = models.TextField(null=True)
    birth_date = models.DateField(null=True)

    is_authorized = models.BooleanField(default=False, editable=False)
    authorized_at = models.DateTimeField(null=True, editable=False)

    display_name = models.CharField(max_length=30, null=True)

    allow_follow = models.BooleanField(default=True)
    adult_content = models.BooleanField(default=True)
    content_visibility = models.BooleanField(default=True)
    communities_visibility = models.BooleanField(default=True)

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class ProfileAvatar(models.Model):

    is_active = models.BooleanField(default=False, editable=False)
    image = models.ImageField(
        upload_to=upload_profile_image_to,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    profile = models.OneToOneField(
        "Profile",
        on_delete=models.CASCADE,
        related_name="avatar",
        editable=False,
    )


class ProfileCover(models.Model):

    is_active = models.BooleanField(default=False, editable=False)
    image = models.ImageField(
        upload_to=upload_cover_image_to,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    profile = models.OneToOneField(
        "Profile", on_delete=models.CASCADE, related_name="cover", editable=False
    )


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reset_password_codes"
    )
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class FollowUser(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="followers",
        editable=False,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="following",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["created_by", "user"]]


class ReportUser(models.Model):
    title = models.CharField(max_length=256)
    report = models.TextField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reported_by",
        editable=False,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reported_users",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["created_by", "user"]]


class BlockUser(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="blocked_by",
        editable=False,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="blocked_users",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["created_by", "user"]]
