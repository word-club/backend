from rest_framework import serializers
from django.contrib.auth import get_user_model

from cover.models import Cover
from avatar.models import Avatar
from comment.models import Comment
from community.models import (
    Community,
    Theme,
    Subscription,
)
from hashtag.serializers import HashtagSerializer
from publication.models import (
    Publication,
)
from share.models import Share
from vote.models import Vote


class CommunityGlobalSerializer(serializers.ModelSerializer):
    tags = HashtagSerializer(many=True)
    avatar = serializers.SerializerMethodField(allow_null=True)
    cover = serializers.SerializerMethodField(allow_null=True)
    theme = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    subscribers_count = serializers.SerializerMethodField()

    @staticmethod
    def get_avatar(obj):
        try:
            avatar = Avatar.objects.get(community=obj, is_active=True)
            return avatar.image.url
        except Avatar.DoesNotExist:
            return None

    @staticmethod
    def get_cover(obj):
        try:
            cover = Cover.objects.get(community=obj, is_active=True)
            return cover.image.url
        except Cover.DoesNotExist:
            return None

    @staticmethod
    def get_theme(obj):
        try:
            theme = Theme.objects.get(community=obj)
            return {
                "color": theme.color,
                "to_call_subscriber": theme.subscriber_nickname,
                "state_after_subscription": theme.state_after_subscription,
            }
        except Theme.DoesNotExist:
            return "primary"

    @staticmethod
    def get_rating(obj):
        # TODO: implement community rating
        return 0

    @staticmethod
    def get_subscribers_count(obj):
        subscribers = Subscription.objects.filter(community=obj).count()
        return subscribers

    class Meta:
        model = Community
        fields = [
            "id",
            "unique_id",
            "created_at",
            "name",
            "quote",
            "avatar",
            "cover",
            "theme",
            "rating",
            "tags",
            "subscribers_count",
        ]


class UserGlobalSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()

    @staticmethod
    def get_name(obj):
        if obj.first_name and obj.last_name:
            return "{} {}".format(obj.first_name, obj.last_name)
        else:
            return False

    @staticmethod
    def get_bio(obj):
        return obj.profile.bio

    @staticmethod
    def get_birth_date(obj):
        return obj.profile.birth_date

    @staticmethod
    def get_avatar(obj):
        try:
            cover = Avatar.objects.get(profile=obj.profile, is_active=True)
            return cover.image.url
        except Avatar.DoesNotExist:
            return None

    @staticmethod
    def get_cover(obj):
        try:
            cover = Cover.objects.get(profile=obj.profile, is_active=True)
            return cover.image.url
        except Cover.DoesNotExist:
            return None

    @staticmethod
    def get_reactions(obj):
        count = 0
        publications = Publication.objects.filter(created_by=obj)
        for pub in publications:
            comments = Comment.objects.filter(publication=pub).count()

            up_votes = Vote.objects.filter(publication=pub, up=True).count()
            down_votes = Vote.objects.filter(publication=pub, up=False).count()
            shares = Share.objects.filter(publication=pub).count()
            count += comments + up_votes + down_votes + shares
        return count

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "bio",
            "date_joined",
            "name",
            "birth_date",
            "avatar",
            "cover",
            "reactions",
        ]


class PublicationForUserCommentSerializer(serializers.ModelSerializer):
    community = CommunityGlobalSerializer()
    created_by = UserGlobalSerializer()

    class Meta:
        model = Publication
        fields = "__all__"
