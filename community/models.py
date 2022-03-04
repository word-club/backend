import uuid

from django.contrib.auth import get_user_model
from django.db import models

from choices import COLOR_CHOICES, COMMUNITY_TYPES
from community.validators import validate_unique_id
from hashtag.models import Hashtag


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["user", "community"]]


class CommunityRule(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="rules", editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_community_rules",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
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
    ban_reason = models.TextField(null=True, editable=False)
    banned_at = models.DateTimeField(null=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["subscriber", "community"]]


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]


class CommunityTheme(models.Model):
    color = models.CharField(choices=COLOR_CHOICES, max_length=32, default="primary")
    subscriber_nickname = models.CharField(max_length=64, default="Subscribers")
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
        related_name="my_community_themes",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Community(models.Model):
    unique_id = models.CharField(
        max_length=64, unique=True, validators=[validate_unique_id]
    )
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256, null=True)
    email = models.EmailField(unique=True, null=True)
    quote = models.TextField(null=True)
    welcome_text = models.TextField(null=True)

    view_globally = models.BooleanField(default=True)
    contains_adult_content = models.BooleanField(default=False)
    type = models.CharField(max_length=64, choices=COMMUNITY_TYPES)

    tags = models.ManyToManyField(
        Hashtag,
        null=True,
        related_name="communities",
    )

    is_authorized = models.BooleanField(default=False, editable=False)
    authorized_at = models.DateTimeField(blank=True, null=True, editable=False)

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_communities",
        editable=False,
    )

    popularity = models.PositiveIntegerField(default=0, editable=False)
    dislikes = models.PositiveIntegerField(default=0, editable=False)
    discussions = models.PositiveIntegerField(default=0, editable=False)
    supports = models.PositiveBigIntegerField(default=0, editable=False)
    views = models.PositiveBigIntegerField(default=0, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def admins(self):
        return CommunityAdmin.objects.filter(community=self.id).distinct()

    @property
    def sub_admins(self):
        return CommunitySubAdmin.objects.filter(community=self.id).distinct()

    @property
    def theme(self):
        return CommunityTheme.objects.get(community=self.id).distinct()

    @property
    def rules(self):
        return CommunityRule.objects.filter(community=self.id).distinct()

    @property
    def subscriptions(self):
        return CommunitySubscription.objects.filter(community=self.id).distinct()

    def __str__(self):
        return self.name
