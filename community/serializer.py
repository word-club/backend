from django.utils import timezone
from rest_framework import serializers

from block.models import Block
from block.serializers import BlockCommunitySerializer
from community.models import *
from avatar.serializers import CommunityAvatarSerializer
from cover.serializers import CommunityCoverSerializer
from report.serializers import ReportSerializer


class CommunityRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityRule
        exclude = ["community"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return CommunityRule.objects.create(**validated_data)


class CommunityHashtagSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    @staticmethod
    def get_name(obj):
        return obj.tag.tag

    class Meta:
        model = CommunityHashtag
        exclude = ["community"]


class CommunityHashtagPostSerializer(serializers.Serializer):
    tags = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Hashtag.objects.all()),
        required=True,
        max_length=16,
    )


class CommunityAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityAdmin
        exclude = ["community"]
        depth = 1

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)


class CommunitySubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunitySubAdmin
        exclude = ["community"]
        depth = 1

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)


class CommunityThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityTheme
        exclude = ["community"]

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
        exclude = ["community"]


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


class CommunitySubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunitySubscription
        exclude = ["community"]


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


class CommunityRetrieveSerializer(serializers.ModelSerializer):
    theme = CommunityThemeSerializer(read_only=True)
    rules = CommunityRuleSerializer(many=True, read_only=True)
    cover = CommunityCoverSerializer(many=False, read_only=True)
    avatar = CommunityAvatarSerializer(many=False, read_only=True)
    hashtags = CommunityHashtagSerializer(many=True, read_only=True)
    create_progress = CreateProgressSerializer(many=True, read_only=True)
    subscriptions = serializers.SerializerMethodField()
    admins = CommunityAdminSerializer(many=True, read_only=True)
    sub_admins = CommunitySubAdminSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()
    reports = ReportSerializer(many=True, read_only=True)

    @staticmethod
    def get_subscriptions(obj):
        subscribers = CommunitySubscription.objects.filter(community=obj)
        notification_disables = CommunitySubscription.objects.filter(
            community=obj, disable_notification=True
        )
        return {
            "subscribers": subscribers.count(),
            "notification_disables": notification_disables.count(),
        }

    def get_subscription(self, obj):
        user = self.context["user"]
        if type(user) == get_user_model():
            try:
                subscription = CommunitySubscription.objects.get(
                    subscriber=user, community=obj
                )
                return CommunitySubscriptionSerializer(subscription).data
            except CommunitySubscription.DoesNotExist:
                return False

    def get_is_blocked(self, obj):
        user = self.context["user"]
        if type(user) == get_user_model():
            try:
                block = Block.objects.get(created_by=user, community=obj)
                return BlockCommunitySerializer(block).data
            except Block.DoesNotExist:
                return False

    class Meta:
        model = Community
        fields = "__all__"
