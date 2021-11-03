from django.utils import timezone
from rest_framework import serializers

from community.models import *
from publication.serializers import PublicationSerializer


class CommunityAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityAvatar
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)


class CommunityCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityCover
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)


class CommunityRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityRule
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(**validated_data)


class ReportCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityReport
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)


class SubscribeCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunitySubscription
        fields = "__all__"

    def create(self, validated_data):
        community = self.context["community"]
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = community
        if community.type == "public":
            validated_data["is_approved"] = True
            validated_data["approved_at"] = timezone.now()
        return super().create(**validated_data)


class DisableNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityDisableNotifications
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(**validated_data)


class CommunityHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityHashtag
        fields = "__all__"

    def create(self, validated_data):
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)


class CommunityAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityAdmin
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)


class CommunityThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityTheme
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().update(instance, validated_data)


class CommunitySerializer(serializers.ModelSerializer):
    hashtags = CommunityHashtagSerializer(many=True, read_only=True)
    admins = CommunityAdminSerializer(many=True, read_only=True)
    rules = CommunityRuleSerializer(many=True, read_only=True)
    avatar = CommunityAvatarSerializer(many=False, read_only=True)
    cover = CommunityCoverSerializer(many=False, read_only=True)
    reports = ReportCommunitySerializer(many=True, read_only=True)
    subscribers = SubscribeCommunitySerializer(many=True, read_only=True)
    publications = PublicationSerializer(many=True, read_only=True)

    class Meta:
        model = Community
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.Meta.depth = self.context.get('depth', 0)

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(**validated_data)


class CommunityGlobalSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(allow_null=True)

    @staticmethod
    def get_avatar(obj):
        avatar = CommunityAvatar.objects.filter(community=obj, is_active=True)
        return avatar[0].image if len(avatar) > 0 else None

    class Meta:
        model = Community
        fields = ["id", "name", "avatar"]
