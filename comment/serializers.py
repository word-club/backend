from rest_framework import serializers

from comment.models import Comment
from globals import PublicationForUserCommentSerializer, UserGlobalSerializer
from image.serializers import CommentImageSerializer


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        validated_data["publication"] = self.context["publication"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class ReplyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        comment = self.context["comment"]
        validated_data["reply"] = comment
        validated_data["publication"] = comment.publication
        validated_data["created_by"] = self.context["user"]
        return super().create(validated_data)


class ReplySerializer(serializers.ModelSerializer):
    created_by = UserGlobalSerializer()

    class Meta:
        model = Comment
        exclude = ["reply"]


class CommentForProfileSerializer(serializers.ModelSerializer):
    publication = PublicationForUserCommentSerializer()
    images = CommentImageSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        exclude = ["created_by"]


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)
    images = CommentImageSerializer(many=True, read_only=True)
    created_by = UserGlobalSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
