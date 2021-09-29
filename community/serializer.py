from rest_framework import serializers

from community.models import *


class CommunityAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityAvatar
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"].id
        return super().create(validated_data)


class CommunityCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityCover
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"].id
        return super().create(validated_data)


class CommunityRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityRule
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"].id
        return super().create(**validated_data)


class ReportCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityReport
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"].id
        return super().create(validated_data)


class SubscribeCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunitySubscription
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"].id
        return super().create(**validated_data)


class DisableNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityDisableNotifications
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"].id
        return super().create(**validated_data)


class CommunitySerializer(serializers.ModelSerializer):
    rules = CommunityRuleSerializer(many=True, read_only=True)
    avatars = CommunityAvatarSerializer(many=True, read_only=True)
    covers = CommunityCoverSerializer(many=True, read_only=True)
    reports = ReportCommunitySerializer(many=True, read_only=True)
    subscribers = SubscribeCommunitySerializer(many=True, read_only=True)

    class Meta:
        model = Community
        fields = "__all__"

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
