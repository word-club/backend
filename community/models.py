import os
import random
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from backend.settings import ALLOWED_IMAGES_EXTENSIONS
from hashtag.models import HashTag


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

    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=512, unique=True)
    email = models.EmailField(unique=True)

    is_authorized = models.BooleanField(default=False, editable=False)
    authorized_at = models.DateTimeField(blank=True, null=True, editable=False)

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="created_communities",
        editable=False,
    )
    date_of_registration = models.DateTimeField(auto_now_add=True)

    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-timestamp"]


class CommunityAvatar(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    is_active = models.BooleanField(default=False, editable=False)
    image = models.ImageField(
        upload_to=upload_avatar_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="avatars", editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="created_community_avatars",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class CommunityCover(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to=upload_cover_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="covers", editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="created_community_covers",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class CommunityRule(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    rule = models.TextField()
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="rules", editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="created_community_rules",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class CommunitySubscription(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    subscriber = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="subscribed_communities",
        editable=False,
    )
    community = models.ForeignKey(
        "Community",
        on_delete=models.CASCADE,
        related_name="subscribers",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["subscriber", "community"]]


class CommunityReport(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    reason = models.TextField()
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reported_communities",
        editable=False,
    )
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="reports", editable=False
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class CommunityDisableNotifications(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="notifications_disabled_communities",
        editable=False,
    )
    community = models.ForeignKey(
        "Community",
        on_delete=models.CASCADE,
        related_name="notifications_disabled_by",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["created_by", "community"]]


class CommunityHashtag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    tag = models.ForeignKey(
        HashTag, related_name="communities", on_delete=models.CASCADE
    )
    publication = models.ForeignKey(
        "Community", related_name="hashtags", on_delete=models.CASCADE, editable=False
    )


class CommunityAdmin(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="admins"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="managed_communities"
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="created_community_admins",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class CommunityAuthorizationCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    community = models.ForeignKey(
        "Community",
        editable=False,
        on_delete=models.CASCADE,
        related_name="authorization_codes"
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="requested_community_authorization_codes",
        editable=False
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
