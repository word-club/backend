from django.utils import timezone
from rest_framework import serializers

from community.models import *


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
        return CommunityRule.objects.create(**validated_data)


class ReportCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityReport
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)


class DisableNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityDisableNotifications
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(**validated_data)


class CommunityHashtagSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    @staticmethod
    def get_name(obj):
        return obj.tag.tag

    class Meta:
        model = CommunityHashtag
        fields = "__all__"


class CommunityHashtagPostSerializer(serializers.Serializer):
    tags = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Hashtag.objects.all()),
        required=True,
        max_length=16,
    )


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


class CreateProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityCreateProgress
        fields = "__all__"


class CommunitySerializer(serializers.ModelSerializer):
    hashtags = CommunityHashtagSerializer(many=True, read_only=True)
    rules = CommunityRuleSerializer(many=True, read_only=True)
    avatar = CommunityAvatarSerializer(many=False, read_only=True)
    cover = CommunityCoverSerializer(many=False, read_only=True)
    create_progress = CreateProgressSerializer(many=True, read_only=True)
    theme = CommunityThemeSerializer(read_only=True)

    class Meta:
        model = Community
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = self.context.get("depth", 0)

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Community.objects.create(**validated_data)


class SubscribeCommunitySerializer(serializers.ModelSerializer):
    community = CommunitySerializer(read_only=True)
    class Meta:
        model = CommunitySubscription
        fields = "__all__"
        depth = 2

    def create(self, validated_data):
        community = self.context["community"]
        validated_data["subscriber"] = self.context["request"].user
        validated_data["community"] = community
        if community.type == "public":
            validated_data["is_approved"] = True
            validated_data["approved_at"] = timezone.now()
        return CommunitySubscription.objects.create(**validated_data)
