from collections import OrderedDict

from rest_framework import serializers
from django.contrib.auth import get_user_model

from community.serializers.theme import ThemeSerializer
from cover.models import Cover
from avatar.models import Avatar
from comment.models import Comment
from community.models import (
    Community,
    Subscription,
)
from hashtag.serializers import HashtagSerializer
from helpers.get_active import get_active_cover_for, get_active_avatar_for
from helpers.publication import get_thumbnail_for
from publication.models import (
    Publication,
)
from share.models import Share
from vote.models import Vote


class CommunityGlobalSerializer(serializers.ModelSerializer):
    tags = HashtagSerializer(many=True)
    avatar = serializers.SerializerMethodField(allow_null=True)
    cover = serializers.SerializerMethodField(allow_null=True)
    theme = ThemeSerializer()
    rating = serializers.SerializerMethodField()
    subscribers_count = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        filterset = OrderedDict()
        filterset["community"] = obj.id
        return get_active_avatar_for(filterset, self.context.get('request', None))

    def get_cover(self, obj):
        filterset = OrderedDict()
        filterset["community"] = obj.id
        return get_active_cover_for(filterset, self.context.get('request', None))

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
            "views",
            "type",
            "is_authorized",
            "subscribers_count",
        ]


class UserGlobalSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    popularity = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    discussions = serializers.SerializerMethodField()
    supports = serializers.SerializerMethodField()

    @staticmethod
    def get_popularity(obj):
        return obj.profile.popularity

    @staticmethod
    def get_discussions(obj):
        return obj.profile.discussions

    @staticmethod
    def get_supports(obj):
        return obj.profile.supports

    @staticmethod
    def get_dislikes(obj):
        return obj.profile.dislikes

    @staticmethod
    def get_display_name(obj):
        return obj.profile.display_name

    @staticmethod
    def get_bio(obj):
        return obj.profile.bio

    @staticmethod
    def get_birth_date(obj):
        return obj.profile.birth_date

    def get_avatar(self, obj):
        filterset = OrderedDict()
        filterset["profile"] = obj.profile
        return get_active_avatar_for(filterset, self.context.get("request"))

    def get_cover(self, obj):
        filterset = OrderedDict()
        filterset["profile"] = obj.profile
        return get_active_cover_for(filterset, self.context.get("request"))

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
            "display_name",
            "birth_date",
            "avatar",
            "cover",
            "reactions",
            "popularity",
            "discussions",
            "supports",
            "dislikes",
        ]


class PublicationGlobalSerializer(serializers.ModelSerializer):
    community = CommunityGlobalSerializer()
    created_by = UserGlobalSerializer()
    thumbnail = serializers.SerializerMethodField()

    @staticmethod
    def get_thumbnail(obj):
        return get_thumbnail_for(obj)

    class Meta:
        model = Publication
        exclude = ["content"]


class CommentGlobalSerializer(serializers.ModelSerializer):
    publication = PublicationGlobalSerializer()

    class Meta:
        model = Comment
        fields = "__all__"


class ShareGlobalSerializer(serializers.ModelSerializer):
    publication = PublicationGlobalSerializer()

    class Meta:
        model = Share
        fields = "__all__"
