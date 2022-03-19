from django.contrib.auth import get_user_model
from django.db import models

from django_countries.fields import CountryField

from choices import GENDER_CHOICES


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, editable=False)
    bio = models.TextField(null=True)
    birth_date = models.DateField(null=True)

    is_authorized = models.BooleanField(default=False, editable=False)
    authorized_at = models.DateTimeField(null=True, editable=False)

    display_name = models.CharField(max_length=30, null=True)

    allow_follow = models.BooleanField(default=True)
    adult_content = models.BooleanField(default=True)
    content_visibility = models.BooleanField(default=True)
    communities_visibility = models.BooleanField(default=True)

    popularity = models.PositiveIntegerField(default=0, editable=False)
    dislikes = models.PositiveIntegerField(default=0, editable=False)
    discussions = models.PositiveIntegerField(default=0, editable=False)
    supports = models.PositiveBigIntegerField(default=0, editable=False)

    country = CountryField(null=True, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deactivated = models.BooleanField(default=False, editable=False)
    deactivated_at = models.DateTimeField(null=True, editable=False)
    deactivation_reason = models.CharField(max_length=255, null=True, editable=False)

    class Meta:
        ordering = ["-created_at"]


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["created_by", "user"]]


class Gender(models.Model):
    custom = models.CharField(max_length=16, null=True)
    type = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, editable=False)
