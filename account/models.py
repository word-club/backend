import os
import random
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, editable=False
    )
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ProfileAvatar(models.Model):
    is_active = models.BooleanField(default=False, editable=False)
    image = models.ImageField(
        upload_to=upload_profile_image_to,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="images"
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class ProfileCover(models.Model):
    is_active = models.BooleanField(default=False, editable=False)
    image = models.ImageField(
        upload_to=upload_cover_image_to,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="covers"
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reset_password_codes"
    )
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
