from django.utils import timezone

from rest_framework import serializers

from avatar.serializers import CommunityAvatarSerializer, Avatar
from comment.serializers import Comment
from community.models import Community
from community.serializers.moderator import ModeratorSerializer
from community.serializers.rule import RuleSerializer
from community.serializers.subscription import SubscriptionCommunitySerializer
from community.serializers.theme import ThemeSerializer
from cover.serializers import CommunityCoverSerializer, Cover
from hashtag.serializers import HashtagSerializer
from report.serializers import ReportSerializer


def get_active_community_avatar(community):
    try:
        avatar = Avatar.objects.get(community=community, is_active=True)
        return CommunityAvatarSerializer(avatar).data
    except Avatar.DoesNotExist:
        return None


def get_active_community_cover(community):
    try:
        cover = Cover.objects.get(community=community, is_active=True)
        return CommunityCoverSerializer(cover).data
    except Cover.DoesNotExist:
        return None


class MyCommunitySerializer(serializers.ModelSerializer):
    theme = ThemeSerializer(read_only=True)
    rules = RuleSerializer(many=True, read_only=True)
    avatar = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    tags = HashtagSerializer(many=True, read_only=True)
    moderators = ModeratorSerializer(many=True, read_only=True)
    subscriptions = SubscriptionCommunitySerializer(many=True, read_only=True)
    reports = ReportSerializer(many=True, read_only=True)

    def get_avatar(self, obj):
        return get_active_community_avatar(obj)

    def get_cover(self, obj):
        return get_active_community_cover(obj)

    class Meta:
        model = Community
        exclude = ["created_by"]


class TrendingSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    theme = ThemeSerializer(read_only=True)

    discussions_today = serializers.SerializerMethodField()

    def get_discussions_today(self, obj):
        # TODO: check if publication is not banned
        return Comment.objects.filter(
            publication__community=obj, created_at__day=timezone.now().day
        ).count()

    def get_avatar(self, obj):
        return get_active_community_avatar(obj)

    def get_cover(self, obj):
        return get_active_community_cover(obj)

    class Meta:
        model = Community
        fields = ["id", "name", "avatar", "unique_id", "cover", "theme", "discussions_today"]


class CommunitySerializer(serializers.ModelSerializer):
    tags = HashtagSerializer(many=True, read_only=True)
    rules = RuleSerializer(many=True, read_only=True)
    avatars = CommunityAvatarSerializer(many=True, read_only=True)
    covers = CommunityCoverSerializer(many=True, read_only=True)
    theme = ThemeSerializer(read_only=True)
    moderators = ModeratorSerializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = self.context.get("depth", 0)

    class Meta:
        model = Community
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Community.objects.create(**validated_data)


class RetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a community
    """

    theme = ThemeSerializer(read_only=True)
    rules = RuleSerializer(many=True, read_only=True)
    covers = CommunityCoverSerializer(many=True, read_only=True)
    avatars = CommunityAvatarSerializer(many=True, read_only=True)
    tags = HashtagSerializer(many=True, read_only=True)
    moderators = ModeratorSerializer(many=True, read_only=True)
    subscriptions = SubscriptionCommunitySerializer(many=True, read_only=True)
    reports = ReportSerializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = self.context.get("depth", 0)

    class Meta:
        model = Community
        fields = "__all__"
