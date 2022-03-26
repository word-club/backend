from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint


def get_constraints(model):
    return [
        UniqueConstraint(
            fields=["publication", "created_by"],
            condition=models.Q(publication__isnull=False),
            name=f"unique_publication_user_{model}",
        ),
        UniqueConstraint(
            fields=["comment", "created_by"],
            condition=models.Q(comment__isnull=False),
            name=f"unique_comment_user_{model}",
        ),
        UniqueConstraint(
            fields=["profile", "created_by"],
            condition=models.Q(profile__isnull=False),
            name=f"unique_profile_user_{model}",
        ),
        UniqueConstraint(
            fields=["community", "created_by"],
            condition=models.Q(community__isnull=False),
            name=f"unique_community_user_{model}",
        ),
    ]


def check_assignment(self, keys: list):
    check = 0
    for key in keys:
        if getattr(self, key, None):
            check += 1
    if check == 0:
        raise ValidationError({"detail": "One of the key field must be specified"})
    if check > 1:
        raise ValidationError({"detail": "Only one key field can be submitted"})


def check_for_mains_unique_model_assignment(self, extra_keys=None):
    if extra_keys is None:
        extra_keys = []
    check_assignment(self, ["publication", "comment", "profile", "community"] + extra_keys)


class Reactions(models.Model):
    popularity = models.PositiveIntegerField(default=0, editable=False)
    dislikes = models.PositiveIntegerField(default=0, editable=False)
    discussions = models.PositiveIntegerField(default=0, editable=False)
    supports = models.PositiveBigIntegerField(default=0, editable=False)
    views = models.PositiveBigIntegerField(default=0, editable=False)

    class Meta:
        abstract = True


class Mains(models.Model):
    profile = models.ForeignKey(
        "account.Profile",
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        null=True,
        editable=False,
    )
    community = models.ForeignKey(
        "community.Community",
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        null=True,
        editable=False,
    )
    publication = models.ForeignKey(
        "publication.Publication",
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        null=True,
        editable=False,
    )
    comment = models.ForeignKey(
        "comment.Comment",
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        null=True,
        editable=False,
    )

    class Meta:
        abstract = True
