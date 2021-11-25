import os
import random
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db import models
from backend.settings import ALLOWED_IMAGES_EXTENSIONS
from choices import COMMUNITY_TYPES, PROGRESS_STATES, COLOR_CHOICES
from hashtag.models import Hashtag


def upload_avatar_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"communities/{instance.community.pk}/avatar/{filename}"


def upload_cover_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"communities/{instance.community.pk}/cover/{filename}"


def validate_unique_id(value):
    items_to_ignore = ["\\", " ", "#", "?", "/", "&", "^", "%", "@", "!"]
    for item in items_to_ignore:
        if item in value:
            raise ValidationError(", ".join(items_to_ignore) + " are not allowed.")


class Community(models.Model):

    unique_id = models.CharField(
        max_length=64, unique=True, validators=[validate_unique_id]
    )
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256, null=True)
    email = models.EmailField(unique=True, null=True)

    is_authorized = models.BooleanField(default=False, editable=False)
    authorized_at = models.DateTimeField(blank=True, null=True, editable=False)
    type = models.CharField(max_length=64, choices=COMMUNITY_TYPES)

    completed_registration_steps = models.BooleanField(default=False, editable=False)

    contains_adult_content = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="created_communities",
        editable=False,
    )
    date_of_registration = models.DateTimeField(auto_now_add=True)

    timestamp = models.DateTimeField(auto_now=True)

    quote = models.TextField(null=True)
    welcome_text = models.TextField(null=True)

    class Meta:
        ordering = ["-timestamp"]


class CommunityCreateProgress(models.Model):
    community = models.ForeignKey(
        "Community",
        on_delete=models.CASCADE,
        related_name="create_progress",
        editable=False,
    )
    state = models.CharField(max_length=64, choices=PROGRESS_STATES)
    is_completed = models.BooleanField(default=False)
    is_skipped = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["timestamp"]


class CommunityAvatar(models.Model):
    image = models.ImageField(
        upload_to=upload_avatar_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    community = models.OneToOneField(
        "Community", on_delete=models.CASCADE, related_name="avatar", editable=False
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
    image = models.ImageField(
        upload_to=upload_cover_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    community = models.OneToOneField(
        "Community", on_delete=models.CASCADE, related_name="cover", editable=False
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

    title = models.CharField(max_length=64)
    description = models.TextField()
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
        ordering = ["timestamp"]
        unique_together = [["community", "title"]]


class CommunitySubscription(models.Model):

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

    disable_notification = models.BooleanField(default=False, editable=False)

    is_approved = models.BooleanField(default=False, editable=False)
    approved_at = models.DateTimeField(null=True, editable=False)

    is_banned = models.BooleanField(default=False, editable=False)
    banned_at = models.DateTimeField(null=True, editable=False)

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["subscriber", "community"]]


class CommunityReport(models.Model):

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


class CommunityHashtag(models.Model):

    tag = models.ForeignKey(
        Hashtag, related_name="communities", on_delete=models.CASCADE
    )
    community = models.ForeignKey(
        "Community", related_name="hashtags", on_delete=models.CASCADE, editable=False
    )

    class Meta:
        unique_together = [["tag", "community"]]


class CommunityAdmin(models.Model):
    is_accepted = models.BooleanField(default=False, editable=False)
    accepted_at = models.DateTimeField(null=True, editable=False)
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="admins", editable=False
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
        unique_together = [["user", "community"]]


class CommunitySubAdmin(models.Model):

    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="sub_admins", editable=False
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="sub_managed_communities",
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="created_community_sub_admins",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = [["user", "community"]]


class CommunityAuthorizationCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    community = models.ForeignKey(
        "Community",
        editable=False,
        on_delete=models.CASCADE,
        related_name="authorization_codes",
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="requested_community_authorization_codes",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class CommunityTheme(models.Model):
    color = models.CharField(choices=COLOR_CHOICES, max_length=32, default="primary")
    to_call_subscriber = models.CharField(max_length=64, default="Subscribers")
    state_after_subscription = models.CharField(max_length=64, default="Awesome")
    community = models.OneToOneField(
        "Community",
        editable=False,
        on_delete=models.CASCADE,
        related_name="theme",
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="added_themes",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
