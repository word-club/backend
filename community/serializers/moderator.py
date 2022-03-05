from rest_framework import serializers

from community.sub_models.moderator import Moderator


class ModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderator
        exclude = ["community", "role", "created_by"]

    def create(self, validated_data):
        validated_data["role"] = self.context["request"].role
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)


class MyModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderator
        exclude = ["created_by"]
