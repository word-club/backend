from rest_framework import serializers

from avatar.models import Avatar
from globals import UserGlobalSerializer


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = "__all__"


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        exclude = ("profile", "community")

    def create(self, validated_data):
        validated_data["profile"] = self.context["profile"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class CommunityAvatarSerializer(serializers.ModelSerializer):
    created_by = UserGlobalSerializer(read_only=True)

    class Meta:
        model = Avatar
        exclude = ("profile", "community")

    def create(self, validated_data):
        validated_data["community"] = self.context["community"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
