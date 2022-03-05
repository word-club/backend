from django.contrib.auth import get_user_model
from django.db import models

from choices import COMMUNITY_TYPES
from community.validators import validate_unique_id
from hashtag.models import Hashtag

from community.sub_models.moderator import Moderator
from community.sub_models.rule import Rule
from community.sub_models.theme import Theme
from community.sub_models.subscription import Subscription


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
    def moderators(self):
        return Moderator.objects.filter(community=self.id, role="mod").distinct()

    @property
    def sub_moderators(self):
        return Moderator.objects.filter(community=self.id, role="sub").distinct()

    @property
    def theme(self):
        return Theme.objects.get(community=self.id).distinct()

    @property
    def rules(self):
        return Rule.objects.filter(community=self.id).distinct()

    @property
    def subscriptions(self):
        return Subscription.objects.filter(community=self.id).distinct()

    def __str__(self):
        return self.name
