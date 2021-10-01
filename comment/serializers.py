from rest_framework import serializers

import helper
from comment.models import *


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = "__all__"

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        return super().create(validated_data)


class CommentImageUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImageUrl
        fields = "__all__"

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        return super().create(validated_data)


class CommentVideoUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentVideoUrl
        fields = "__all__"

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        return super().create(validated_data)


class CommentUpVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentUpVote
        fields = "__all__"

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class CommentDownVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentDownVote
        fields = "__all__"

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class CommentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportComment
        fields = "__all__"

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = "__all__"

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class CommentPostSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        max_length=3,
        required=False
    )
    image_urls = serializers.ListField(
        child=serializers.URLField(),
        max_length=3,
        required=False
    )
    video_urls = serializers.ListField(
        child=serializers.URLField(),
        max_length=3,
        required=False
    )

    @staticmethod
    def validate_images(obj):
        helper.check_images_size_with_ext(obj)
        return obj

    class Meta:
        model = Comment
        fields = ["comment", "publication", "images", "image_urls", "video_urls"]

    def create(self, validated_data):
        comment = Comment.objects.create(
            comment=validated_data["comment"],
            publication=self.context["publication"],
            created_by=self.context["request"].user
        )

        images = validated_data.get("images")
        if images: [CommentImage.objects.create(comment=comment, image=image) for image in images]

        image_urls = validated_data.get("image_urls")
        if image_urls: [CommentImageUrl.objects.create(comment=comment, url=url) for url in image_urls]

        video_urls = validated_data.get("video_urls")
        if video_urls: [CommentVideoUrl.objects.create(comment=comment, url=url) for url in video_urls]

        return comment


class CommentSerializer(serializers.ModelSerializer):
    replies = CommentReplySerializer(many=True, read_only=True)
    images = CommentImageSerializer(many=True, read_only=True)
    image_urls = CommentImageUrlSerializer(many=True, read_only=True)
    video_urls = CommentVideoUrlSerializer(many=True, read_only=True)
    up_votes = CommentUpVoteSerializer(many=True, read_only=True)
    down_votes = CommentDownVoteSerializer(many=True, read_only=True)
    reports = CommentReportSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
