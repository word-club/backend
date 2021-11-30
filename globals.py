from rest_framework import serializers
from django.contrib.auth import get_user_model

from account.models import ProfileCover, ProfileAvatar
from comment.models import Comment
from community.models import (
    Community,
    CommunityAvatar,
    CommunityTheme,
    CommunityCover,
    CommunitySubscription, CommunityHashtag,
)
from publication.models import (
    Publication,
    PublicationUpVote,
    PublicationShare,
    PublicationDownVote,
)


class CommunityGlobalSerializer(serializers.ModelSerializer):
    hashtags = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField(allow_null=True)
    cover = serializers.SerializerMethodField(allow_null=True)
    theme = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    subscribers_count = serializers.SerializerMethodField()

    @staticmethod
    def get_avatar(obj):
        try:
            avatar = CommunityAvatar.objects.get(community=obj)
            return avatar.image.url
        except CommunityAvatar.DoesNotExist:
            return None

    @staticmethod
    def get_cover(obj):
        try:
            cover = CommunityCover.objects.get(community=obj)
            return cover.image.url
        except CommunityCover.DoesNotExist:
            return None

    @staticmethod
    def get_theme(obj):
        try:
            theme = CommunityTheme.objects.get(community=obj)
            return {
                "color": theme.color,
                "to_call_subscriber": theme.to_call_subscriber,
                "state_after_subscription": theme.state_after_subscription,
            }
        except CommunityTheme.DoesNotExist:
            return "primary"

    @staticmethod
    def get_rating(obj):
        # TODO: implement community rating
        return 0

    @staticmethod
    def get_subscribers_count(obj):
        subscribers = CommunitySubscription\
            .objects.filter(community=obj).count()
        return subscribers

    @staticmethod
    def get_hashtags(obj):
        tags = CommunityHashtag\
            .objects.filter(community=obj)
        dataset = []
        for tag in tags:
            dataset.append({"id": tag.id, "tag": tag.tag.id, "name": tag.tag.tag})
        return dataset

    class Meta:
        model = Community
        fields = [
            "id",
            "unique_id",
            "date_of_registration",
            "name",
            "quote",
            "avatar",
            "cover",
            "theme",
            "rating",
            "hashtags",
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
            cover = ProfileAvatar.objects.get(profile=obj.profile)
            return cover.image.url
        except ProfileAvatar.DoesNotExist:
            return None

    @staticmethod
    def get_cover(obj):
        try:
            cover = ProfileCover.objects.get(profile=obj.profile)
            return cover.image.url
        except ProfileCover.DoesNotExist:
            return None

    @staticmethod
    def get_reactions(obj):
        count = 0
        publications = Publication.objects.filter(created_by=obj)
        for pub in publications:
            comments = Comment.objects.filter(publication=pub).count()

            up_votes = PublicationUpVote.objects.filter(publication=pub).count()
            down_votes = PublicationDownVote.objects.filter(publication=pub).count()
            shares = PublicationShare.objects.filter(publication=pub).count()
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
