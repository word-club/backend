from rest_framework import serializers

from cover.models import Cover
from globals import UserGlobalSerializer


class CoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cover
        fields = "__all__"


class ProfileCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cover
        exclude = ("community", "profile")

    def create(self, validated_data):
        validated_data["profile"] = self.context["profile"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class CommunityCoverSerializer(serializers.ModelSerializer):
    created_by = UserGlobalSerializer(read_only=True)

    class Meta:
        model = Cover
        exclude = ("profile",)

    def create(self, validated_data):
        validated_data["community"] = self.context["community"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
