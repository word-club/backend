from rest_framework import serializers

from comment.serializers import CommentSerializer
from globals import CommunityGlobalSerializer, UserGlobalSerializer
from hashtag.serializers import HashtagSerializer
from image.serializers import PublicationImageSerializer
from link.serializers import LinkInfoSerializer
from publication.models import Publication


class PublicationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["user"]
        publication = Publication.objects.create(**validated_data)
        # TODO: link hashtags to the publication
        # for hashtag in hashtags:
        # publication.hash_tags.add(hashtag)
        return publication


class PublicationSerializer(serializers.ModelSerializer):
    community = CommunityGlobalSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    links = LinkInfoSerializer(read_only=True)
    images = PublicationImageSerializer(read_only=True, many=True)
    tags = HashtagSerializer(read_only=True, many=True)
    created_by = UserGlobalSerializer(read_only=True)

    class Meta:
        model = Publication
        fields = "__all__"
