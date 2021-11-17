import metadata_parser
from rest_framework import serializers

from comment.serializers import CommentSerializer
from helper import get_twitter_embed_data
from publication.models import *


class PublicationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationImage
        fields = "__all__"

    def create(self, validated_data):
        validated_data["publication"] = self.context["publication"]
        return super().create(validated_data)


class PublicationLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationLink
        fields = "__all__"

    def create(self, validated_data):
        validated_data["publication"] = self.context["publication"]
        page = metadata_parser.MetadataParser(
            url=validated_data.get("link")
        )
        image = page.get_metadata_link('image', allow_encoded_uri=True)
        page_title = page.get_metadatas('title', strategy=['page', 'og', 'dc',])
        page_desc = page.get_metadatas('description', strategy=['page', 'og', 'dc',])
        validated_data['image'] = image
        validated_data['title'] = page_title[0] if page_title else None
        validated_data['description'] = page_desc[0] if page_desc else None
        return super().create(validated_data)

    def update(self, instance, validated_data):
        page = metadata_parser.MetadataParser(
            url=validated_data.get("link")
        )
        image = page.get_metadata_link('image', allow_encoded_uri=True)
        page_title = page.get_metadatas('title', strategy=['page', 'og', 'dc', ])
        page_desc = page.get_metadatas('description', strategy=['page', 'og', 'dc', ])
        validated_data['image'] = image
        validated_data['title'] = page_title[0] if page_title else None
        validated_data['description'] = page_desc[0] if page_desc else None
        return super().update(instance, validated_data)


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
    link = PublicationLinkSerializer(read_only=True)
    images = PublicationImageSerializer(read_only=True, many=True)
    image_urls = PublicationImageUrlSerializer(read_only=True, many=True)
    up_votes = PublicationUpVoteSerializer(read_only=True, many=True)
    down_votes = PublicationDownVoteSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Publication
        fields = "__all__"
        depth=2

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class BookmarkedPublicationsSerializers(serializers.ModelSerializer):
    publication = PublicationSerializer(read_only=True)

    class Meta:
        model = PublicationBookmark
        fields = "__all__"

class TwitterOEmbedData:
    def __init__(self, source, oembed):
        self.source = source
        self.oembed = oembed


class TwitterEmbedSerializer(serializers.Serializer):
    source = serializers.URLField()
    oembed = serializers.JSONField()
