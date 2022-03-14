from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

from rest_framework import serializers

from account.models import Profile
from account.serializers.follow import FollowingSerializer, FollowerSerializer
from avatar.serializers import ProfileAvatarSerializer
from bookmark.serializers import MyBookmarkSerializer
from comment.serializers import MyCommentSerializer
from community.serializers.community import MyCommunitySerializer
from community.serializers.moderator import MyModerationSerializer
from community.serializers.subscription import MySubscriptionSerializer
from cover.serializers import ProfileCoverSerializer
from hide.serializers import MyHideSerializer
from notification.serializers import MyNotificationSerializer
from publication.serializers import MyPublicationSerializer, Publication
from report.serializers import MyReportSerializer
from share.serializers import MyShareSerializer
from vote.serializers import MyVoteSerializer


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


class ProfileSerializer(serializers.ModelSerializer):
    avatars = ProfileAvatarSerializer(read_only=True, many=True)
    covers = ProfileCoverSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        exclude = ["user"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        exclude = ["password"]


class UserRetrieveSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    followers = FollowerSerializer(many=True, read_only=True)
    following = FollowingSerializer(many=True, read_only=True)
    my_comments = MyCommentSerializer(many=True, read_only=True)
    my_publications = serializers.SerializerMethodField()
    my_subscriptions = MySubscriptionSerializer(many=True, read_only=True)

    @staticmethod
    def get_my_publications(obj):
        publications = Publication.objects.filter(created_by=obj, is_published=True)
        return MyPublicationSerializer(publications, many=True).data

    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserInfoSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    followers = FollowerSerializer(many=True, read_only=True)
    following = FollowingSerializer(many=True, read_only=True)

    my_publications = MyPublicationSerializer(many=True, read_only=True)
    my_votes = MyVoteSerializer(many=True, read_only=True)
    my_shares = MyShareSerializer(many=True, read_only=True)
    my_bookmarks = MyBookmarkSerializer(many=True, read_only=True)
    my_comments = MyCommentSerializer(many=True, read_only=True)
    my_reports = MyReportSerializer(many=True, read_only=True)
    my_hides = MyHideSerializer(many=True, read_only=True)
    my_communities = MyCommunitySerializer(many=True, read_only=True)
    my_subscriptions = MySubscriptionSerializer(many=True, read_only=True)
    managed_communities = MyModerationSerializer(many=True, read_only=True)

    received_notifications = MyNotificationSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = "__all__"
