from rest_framework import serializers

from cover.models import Cover


class CoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cover
        fields = "__all__"


class ProfileCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cover
        exclude = ("community",)

    def create(self, validated_data):
        validated_data["profile"] = self.context["profile"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class CommunityCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cover
        exclude = ("profile",)

    def create(self, validated_data):
        validated_data["community"] = self.context["community"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
