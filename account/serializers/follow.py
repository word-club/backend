from rest_framework import serializers

from account.models import FollowUser


class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        fields = "__all__"

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data["to_follow"] = self.context["to_follow"]
        return super().create(validated_data)
