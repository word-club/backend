from rest_framework import serializers

from comment.serializers import CommentSerializer
from publication.models import *


class PublicationHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationHashtag
        fields = "__all__"

    def create(self, validated_data):
        validated_data["publication"] = self.context["publication"]
        return super().create(validated_data)


class PublicationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationImage
        fields = "__all__"

    def create(self, validated_data):
        validated_data["publication"] = self.context["publication"]
        return super().create(validated_data)


class PublicationImageUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationImageUrl
        fields = "__all__"

    def create(self, validated_data):
        validated_data["publication"] = self.context["publication"]
        return super().create(validated_data)


class PublicationUpVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationUpVote
        fields = "__all__"


class PublicationDownVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationDownVote
        fields = "__all__"


class PublicationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportPublication
        fields = "__all__"

    def create(self, validated_data):
        validated_data["publication"] = self.context["publication"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class PublicationSerializer(serializers.ModelSerializer):
    hashtags = PublicationHashtagSerializer(read_only=True, many=True)
    images = PublicationImageSerializer(read_only=True, many=True)
    image_urls = PublicationImageUrlSerializer(read_only=True, many=True)
    up_votes = PublicationUpVoteSerializer(read_only=True, many=True)
    down_votes = PublicationDownVoteSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Publication
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class BookmarkedPublicationsSerializers(serializers.ModelSerializer):
    publication = PublicationSerializer(read_only=True)

    class Meta:
        model = PublicationBookmark
        fields = "__all__"
