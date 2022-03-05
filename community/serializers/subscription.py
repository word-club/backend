from django.utils import timezone

from rest_framework import serializers

from community.sub_models.subscription import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class SubscribeCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        exclude = ["community"]
        depth = 2

    def create(self, validated_data):
        community = self.context["community"]
        validated_data["subscriber"] = self.context["request"].user
        validated_data["community"] = community
        if community.type == "public":
            validated_data["is_approved"] = True
            validated_data["approved_at"] = timezone.now()
        return super().create(validated_data)
