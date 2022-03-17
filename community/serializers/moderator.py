from rest_framework import serializers

from community.sub_models.moderator import Moderator
from globals import CommunityGlobalSerializer, UserGlobalSerializer


class ModeratorSerializer(serializers.ModelSerializer):
    user = UserGlobalSerializer(read_only=True)

    class Meta:
        model = Moderator
        exclude = ["community", "created_by"]
        read_only_fields = ["role"]

    def create(self, validated_data):
        validated_data["role"] = self.context["request"].role
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)


class MyModerationSerializer(serializers.ModelSerializer):
    community = CommunityGlobalSerializer()

    class Meta:
        model = Moderator
        exclude = ["user"]
