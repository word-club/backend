from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from account.models import *
from account.serializers.follow import FollowUserSerializer
from bookmark.models import Bookmark
from comment.models import Comment
from comment.serializers import (
    CommentSerializer,
    CommentForProfileSerializer,
)
from community.models import CommunitySubscription
from community.serializer import (
    CommunitySerializer,
    CommunityAdminSerializer,
    CommunitySubAdminSerializer,
)
from globals import UserGlobalSerializer
from hide.models import Hide
from notification.serializers import NotificationReceiverSerializer
from publication.models import Publication
from publication.serializers import PublicationSerializer
from report.serializers import ReportSerializer
from share.serializers import ShareSerializer
from vote.models import Vote


class ProfilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UserPostSerializer(serializers.ModelSerializer):
    profile = ProfilePostSerializer(write_only=True, required=True)

    @staticmethod
    def validate_password(password):
        validate_password(password)
        return password

    class Meta:
        model = get_user_model()
        fields = "__all__"
        read_only_fields = ["is_active", "date_joined", "is_superuser", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        password = validated_data.pop("password")
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()
        user.profile.birth_date = profile_data.get("birth_date")
        user.profile.save()
        return user

    def update(self, instance, validated_data):
        profile = instance.profile
        profile_data = validated_data.pop("profile")
        email = validated_data.get("email")
        if email:
            profile.is_authorized = False
            profile.authorized_at = None
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        return instance


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileAvatar
        fields = "__all__"

    def create(self, validated_data):
        validated_data["profile"] = self.context["profile"]
        return super().create(validated_data)


class ProfileCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileCover
        fields = "__all__"

    def create(self, validated_data):
        validated_data["profile"] = self.context["profile"]
        return super().create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    avatar = ProfileAvatarSerializer(read_only=True)
    cover = ProfileCoverSerializer(read_only=True)

    class Meta:
        model = Profile
        exclude = ["user"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = "__all__"


class BlockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockUser
        fields = "__all__"


class UserRetrieveSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    is_followed = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()

    def get_is_followed(self, obj):
        # context "user" is the requester
        user = self.context["user"]
        if type(user) == get_user_model():
            try:
                follow = FollowUser.objects.get(created_by=user, user=obj)
                return FollowUserSerializer(follow).data
            except FollowUser.DoesNotExist:
                return False

    def get_is_blocked(self, obj):
        # context "user" is the requester
        user = self.context["user"]
        if type(user) == get_user_model():
            try:
                block = BlockUser.objects.get(created_by=user, user=obj)
                return BlockUserSerializer(block).data
            except BlockUser.DoesNotExist:
                return False

    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserInfoSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    published_publications = serializers.SerializerMethodField()
    drafts = serializers.SerializerMethodField()
    saved_publications = serializers.SerializerMethodField()
    up_voted_publications = serializers.SerializerMethodField()
    down_voted_publications = serializers.SerializerMethodField()
    hidden_publications = serializers.SerializerMethodField()
    # TODO: add serializer with publication instance
    shared_publications = ShareSerializer(many=True, read_only=True)

    comments = serializers.SerializerMethodField()
    up_voted_comments = serializers.SerializerMethodField()
    down_voted_comments = serializers.SerializerMethodField()
    added_reports = ReportSerializer(many=True, read_only=True)
    hidden_comments = serializers.SerializerMethodField()
    saved_comments = serializers.SerializerMethodField()
    shared_comments = ShareSerializer(many=True, read_only=True)

    created_communities = CommunitySerializer(many=True, read_only=True)
    subscribed_communities = serializers.SerializerMethodField()
    managed_communities = CommunityAdminSerializer(many=True, read_only=True)
    sub_managed_communities = CommunitySubAdminSerializer(many=True, read_only=True)

    received_notifications = NotificationReceiverSerializer(many=True, read_only=True)

    @staticmethod
    def get_published_publications(obj):
        return PublicationSerializer(
            Publication.objects.filter(created_by=obj, is_published=True),
            many=True,
            read_only=True,
            context={"user": obj},
        ).data

    @staticmethod
    def get_drafts(obj):
        return PublicationSerializer(
            Publication.objects.filter(created_by=obj, is_published=False),
            many=True,
            read_only=True,
            context={"user": obj},
        ).data

    @staticmethod
    def get_saved_publications(obj):
        bookmarks = Bookmark.objects.filter(created_by=obj, publication__isnull=False)
        publications = []
        [publications.append(bookmark.publication) for bookmark in bookmarks]
        return PublicationSerializer(
            publications, many=True, read_only=True, context={"user": obj}
        ).data

    @staticmethod
    def get_up_voted_publications(obj):
        items = Vote.objects.filter(created_by=obj, up=True, publication__isnull=False)
        publications = []
        [publications.append(item.publication) for item in items]
        return PublicationSerializer(
            publications, read_only=True, many=True, context={"user": obj}
        ).data

    @staticmethod
    def get_down_voted_publications(obj):
        items = Vote.objects.filter(created_by=obj, up=False, publication__isnull=False)
        publications = []
        [publications.append(item.publication) for item in items]
        return PublicationSerializer(
            publications, read_only=True, many=True, context={"user": obj}
        ).data

    @staticmethod
    def get_hidden_publications(obj):
        items = Hide.objects.filter(created_by=obj, publication__isnull=False)
        publications = []
        [publications.append(item.publication) for item in items]
        return PublicationSerializer(
            publications, read_only=True, many=True, context={"user": obj}
        ).data

    @staticmethod
    def get_comments(obj):
        return CommentForProfileSerializer(
            Comment.objects.filter(created_by=obj),
            many=True,
            read_only=True,
            context={"user": obj},
        ).data

    @staticmethod
    def get_up_voted_comments(obj):
        items = Vote.objects.filter(created_by=obj, up=True, comment__isnull=False)
        comments = []
        [comments.append(item.comment) for item in items]
        return CommentSerializer(
            comments, many=True, read_only=True, context={"user": obj}
        ).data

    @staticmethod
    def get_down_voted_comments(obj):
        items = Vote.objects.filter(created_by=obj, up=False, comment__isnull=False)
        comments = []
        [comments.append(item.comment) for item in items]
        return CommentSerializer(
            comments, many=True, read_only=True, context={"user": obj}
        ).data

    @staticmethod
    def get_hidden_comments(obj):
        items = Hide.objects.filter(created_by=obj, comment__isnull=False)
        comments = []
        [comments.append(item.comment) for item in items]
        return CommentSerializer(
            comments, many=True, read_only=True, context={"user": obj}
        ).data

    @staticmethod
    def get_saved_comments(obj):
        items = Bookmark.objects.filter(created_by=obj, comment__isnull=False)
        comments = []
        [comments.append(item.comment) for item in items]
        return CommentSerializer(
            comments, many=True, read_only=True, context={"user": obj}
        ).data

    @staticmethod
    def get_subscribed_communities(obj):
        items = CommunitySubscription.objects.filter(subscriber=obj)
        communities = []
        [communities.append(item.community) for item in items]
        return CommunitySerializer(
            communities,
            many=True,
            read_only=True,
        ).data

    @staticmethod
    def get_followers(obj):
        followers = FollowUser.objects.filter(user=obj)
        users = []
        [users.append(item.created_by) for item in followers]
        return UserGlobalSerializer(users, many=True, read_only=True).data

    @staticmethod
    def get_following(obj):
        follows = FollowUser.objects.filter(user=obj)
        users = []
        [users.append(item.created_by) for item in follows]
        return UserGlobalSerializer(users, many=True, read_only=True).data

    @staticmethod
    def get_blocked_users(obj):
        blocks = BlockUser.objects.filter(user=obj)
        users = []
        [users.append(item.created_by) for item in blocks]
        return UserGlobalSerializer(users, many=True, read_only=True).data

    class Meta:
        model = get_user_model()
        fields = "__all__"


class MentionUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    @staticmethod
    def get_username(obj):
        return obj.username

    @staticmethod
    def get_name(obj):
        if obj.first_name and obj.last_name:
            return "{} {}".format(obj.first_name, obj.last_name)
        return obj.username

    @staticmethod
    def get_avatar(obj):
        try:
            avatar = ProfileAvatar.objects.get(profile__user=obj)
            return avatar.image.url
        except ProfileAvatar.DoesNotExist:
            return None

    class Meta:
        model = get_user_model()
        fields = ["id", "name", "username", "avatar"]
