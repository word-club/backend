from django.contrib.auth import get_user_model
from django.db import models

from django_countries.fields import CountryField

from choices import GENDER_CHOICES
from helpers.base_classes import Reactions


class Profile(Reactions):
    bio = models.TextField(null=True)
    birth_date = models.DateField(null=True)
    display_name = models.CharField(max_length=32, null=True)
    country = CountryField(null=True, blank=False)

    is_authorized = models.BooleanField(default=False, editable=False)
    authorized_at = models.DateTimeField(null=True, editable=False)

    allow_follow = models.BooleanField(default=True)
    adult_content = models.BooleanField(default=True)
    content_visibility = models.BooleanField(default=True)
    communities_visibility = models.BooleanField(default=True)

    is_deactivated = models.BooleanField(default=False, editable=False)
    deactivated_at = models.DateTimeField(null=True, editable=False)
    deactivation_reason = models.CharField(max_length=255, null=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, editable=False)

    class Meta:
        ordering = ["-created_at"]


class FollowUser(models.Model):
    profile = models.ForeignKey(
        "Profile",
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["created_by", "profile"]]


class Gender(models.Model):
    custom = models.CharField(max_length=16, null=True)
    type = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True)
    profile = models.OneToOneField("Profile", on_delete=models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.custom or dict(self.type)[self.type]
