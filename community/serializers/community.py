from rest_framework import serializers

from avatar.serializers import CommunityAvatarSerializer
from community.models import Community
from community.serializers.moderator import ModeratorSerializer
from community.serializers.rule import RuleSerializer
from community.serializers.subscription import SubscriptionSerializer
from community.serializers.theme import ThemeSerializer
from cover.serializers import CommunityCoverSerializer
from hashtag.serializers import HashtagSerializer
from report.serializers import ReportSerializer


class CommunitySerializer(serializers.ModelSerializer):
    tags = HashtagSerializer(many=True, read_only=True)
    rules = RuleSerializer(many=True, read_only=True)
    avatar = CommunityAvatarSerializer(many=False, read_only=True)
    cover = CommunityCoverSerializer(many=False, read_only=True)
    theme = ThemeSerializer(read_only=True)

    class Meta:
        model = Community
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Community.objects.create(**validated_data)


class RetrieveSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer(read_only=True)
    rules = RuleSerializer(many=True, read_only=True)
    cover = CommunityCoverSerializer(many=False, read_only=True)
    avatar = CommunityAvatarSerializer(many=False, read_only=True)
    tags = HashtagSerializer(many=True, read_only=True)
    moderators = ModeratorSerializer(many=True, read_only=True)
    subscriptions = SubscriptionSerializer(many=True, read_only=True)
    reports = ReportSerializer(many=True, read_only=True)

    class Meta:
        model = Community
        fields = "__all__"
