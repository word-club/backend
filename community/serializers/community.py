from collections import OrderedDict

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
from helpers.get_active import get_active_avatar_for, get_active_cover_for
from report.serializers import ReportSerializer


class MyCommunitySerializer(serializers.ModelSerializer):
    theme = ThemeSerializer(read_only=True)
    rules = RuleSerializer(many=True, read_only=True)
    avatar = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    tags = HashtagSerializer(many=True, read_only=True)
    moderators = ModeratorSerializer(many=True, read_only=True)
    subscriptions = SubscriptionCommunitySerializer(many=True, read_only=True)
    reports = ReportSerializer(many=True, read_only=True)

    @staticmethod
    def get_avatar(obj):
        filterset = OrderedDict()
        filterset["community"] = obj.id
        return get_active_avatar_for(filterset)

    @staticmethod
    def get_cover(obj):
        filterset = OrderedDict()
        filterset["community"] = obj.id
        return get_active_cover_for(filterset)

    class Meta:
        model = Community
        exclude = ["created_by"]


class TrendingSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    theme = ThemeSerializer(read_only=True)

    discussions_today = serializers.SerializerMethodField()

    @staticmethod
    def get_discussions_today(obj):
        return Comment.objects.filter(
            publication__is_published=True,
            publication__community=obj,
            created_at__day=timezone.now().day,
            # publication__is_banned=False
        ).count()

    @staticmethod
    def get_avatar(obj):
        filterset = OrderedDict()
        filterset["community"] = obj.id
        return get_active_avatar_for(filterset)

    @staticmethod
    def get_cover(obj):
        filterset = OrderedDict()
        filterset["community"] = obj.id
        return get_active_cover_for(filterset)

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
    avatar = serializers.SerializerMethodField(allow_null=True)
    cover = serializers.SerializerMethodField(allow_null=True)
    theme = ThemeSerializer(read_only=True)
    rules = RuleSerializer(many=True, read_only=True)
    covers = CommunityCoverSerializer(many=True, read_only=True)
    avatars = CommunityAvatarSerializer(many=True, read_only=True)
    tags = HashtagSerializer(many=True, read_only=True)
    moderators = ModeratorSerializer(many=True, read_only=True)
    subscriptions = SubscriptionCommunitySerializer(many=True, read_only=True)
    reports = ReportSerializer(many=True, read_only=True)

    @staticmethod
    def get_avatar(obj):
        filterset = OrderedDict()
        filterset["community"] = obj.id
        return get_active_avatar_for(filterset)

    @staticmethod
    def get_cover(obj):
        filterset = OrderedDict()
        filterset["community"] = obj.id
        return get_active_cover_for(filterset)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = self.context.get("depth", 0)

    class Meta:
        model = Community
        fields = "__all__"
