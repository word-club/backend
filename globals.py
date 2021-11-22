from rest_framework import serializers
from django.contrib.auth import get_user_model

from account.models import ProfileCover, ProfileAvatar
from comment.models import Comment
from community.models import Community, CommunityAvatar, CommunityTheme, CommunityCover, CommunitySubscription
from publication.models import Publication, PublicationUpVote, PublicationShare, PublicationDownVote


class CommunityGlobalSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(allow_null=True)
    cover = serializers.SerializerMethodField(allow_null=True)
    theme = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    subscribers = serializers.SerializerMethodField()


    @staticmethod
    def get_avatar(obj):
        try:
            avatar = CommunityAvatar.objects.get(community=obj)
            return avatar.image.url
        except CommunityAvatar.DoesNotExist: return None

    @staticmethod
    def get_cover(obj):
        try:
            cover = CommunityCover.objects.get(community=obj)
            return cover.image.url
        except CommunityCover.DoesNotExist: return None

    @staticmethod
    def get_theme(obj):
        try:
            theme = CommunityTheme.objects.get(community=obj)
            return {
                "color": theme.color,
                "to_call_subscriber": theme.to_call_subscriber,
                "state_after_subscription": theme.state_after_subscription
            }
        except CommunityTheme.DoesNotExist: return "primary"


    def get_reactions(self, obj):
        publications = Publication.objects.filter(community=obj).count()
        return publications

    def get_subscribers(self, obj):
        subscribers = CommunitySubscription.objects.filter(community=obj).count()
        return subscribers


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
            "reactions",
            "subscribers"
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
        else: return False

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
        except ProfileAvatar.DoesNotExist: return None

    @staticmethod
    def get_cover(obj):
        try:
            cover = ProfileCover.objects.get(profile=obj.profile)
            return cover.image.url
        except ProfileCover.DoesNotExist: return None

    @staticmethod
    def get_reactions(obj):
        count = 0
        publications = Publication.objects.filter(created_by=obj)
        for pub in publications:
            comments = Comment.objects.filter(publication=pub).count()

            up_votes = PublicationUpVote.objects.filter(publication=pub).count()
            down_votes = PublicationDownVote.objects.filter(publication=pub).count()
            shares = PublicationShare.objects.filter(publication=pub).count()
            count += (comments + up_votes + down_votes + shares)
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
