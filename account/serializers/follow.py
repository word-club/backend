from rest_framework import serializers

from account.models import FollowUser


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        exclude = ("user",)


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        exclude = ("created_by",)


class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["user"] = self.context["user"]
        return super().create(validated_data)
