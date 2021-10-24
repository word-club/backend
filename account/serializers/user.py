from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

import helper
from account.models import *
from account.serializers.follow import FollowUserSerializer
from community.serializer import CommunityGlobalSerializer
from notification.serializers import NotificationReceiverSerializer
from publication.serializers import (
    PublicationSerializer,
    BookmarkedPublicationsSerializers,
)


class ProfilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UserPostSerializer(serializers.ModelSerializer):
    profile = ProfilePostSerializer(write_only=True, default={})

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
        profile_data = validated_data.get("profile")
        user = get_user_model().objects.create(**validated_data)
        Profile.objects.create(**profile_data, user=user)
        return user

    def update(self, instance, validated_data):
        profile = instance.profile
        profile_data = validated_data.pop("profile")
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
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserInfoSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    followers = FollowUserSerializer(many=True, read_only=True)
    following = FollowUserSerializer(many=True, read_only=True)
    subscribed_communities = CommunityGlobalSerializer(many=True, read_only=True)
    created_publications = PublicationSerializer(many=True, read_only=True)
    received_notifications = NotificationReceiverSerializer(many=True, read_only=True)
    bookmarks = BookmarkedPublicationsSerializers(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = "__all__"
