import os
import random
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from backend.settings import ALLOWED_IMAGES_EXTENSIONS


def upload_avatar_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"communities/{instance.community.pk}/avatar/{filename}"


def upload_cover_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"communities/{instance.community.pk}/cover/{filename}"


class Community(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    email = models.EmailField()
    authorized = models.BooleanField(default=False, editable=False)
    authorized_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)


class CommunityAvatar(models.Model):
    image = models.ImageField(
        upload_to=upload_avatar_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="avatars"
    )
    timestamp = models.DateTimeField(auto_now=True)


class CommunityCover(models.Model):
    image = models.ImageField(
        upload_to=upload_cover_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="covers"
    )
    timestamp = models.DateTimeField(auto_now=True)


class CommunityRule(models.Model):
    rule = models.CharField(max_length=512)
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="rules"
    )
    timestamp = models.DateTimeField(auto_now=True)


class SubscribeCommunity(models.Model):
    is_subscribed = models.BooleanField(default=True)
    subscriber = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="subscribed_communities",
    )
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="subscribers"
    )
    timestamp = models.DateTimeField(auto_now=True)


class ReportCommunity(models.Model):
    reason = models.TextField()
    writer = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reported_communities"
    )
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="reports"
    )
    timestamp = models.DateTimeField(auto_now=True)


class DisableNotifications(models.Model):
    is_disabled = models.BooleanField(default=False)
    writer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="notifications_disabled_communities",
    )
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="notifications_disabled_by"
    )
    timestamp = models.DateTimeField(auto_now=True)
