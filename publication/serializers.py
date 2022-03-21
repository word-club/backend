from rest_framework import serializers

from comment.models import Comment
from comment.serializers import CommentSerializer
from globals import CommunityGlobalSerializer, UserGlobalSerializer
from hashtag.serializers import HashtagSerializer
from image.serializers import PublicationImageSerializer
from link.serializers import LinkInfoSerializer
from publication.models import Publication, RecentPublication


class PublicationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["user"]
        return super().create(validated_data)


class PublicationSerializer(serializers.ModelSerializer):
    community = CommunityGlobalSerializer()
    comments = serializers.SerializerMethodField()
    links = LinkInfoSerializer(read_only=True)
    images = PublicationImageSerializer(read_only=True, many=True)
    tags = HashtagSerializer(read_only=True, many=True)
    created_by = UserGlobalSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = self.context.get("depth", 0)

    @staticmethod
    def get_comments(obj):
        # only include comment items that are not replies
        # replies are included in the parent comment
        comments = Comment.objects.filter(publication=obj, reply=None)
        return CommentSerializer(comments, many=True).data

    class Meta:
        model = Publication
        fields = "__all__"


class MyPublicationSerializer(serializers.ModelSerializer):
    community = CommunityGlobalSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    links = LinkInfoSerializer(read_only=True)
    images = PublicationImageSerializer(read_only=True, many=True)
    tags = HashtagSerializer(read_only=True, many=True)

    class Meta:
        model = Publication
        exclude = ("created_by",)


class PublicationForRecentSerializer(serializers.ModelSerializer):
    tags = HashtagSerializer(read_only=True, many=True)
    community = CommunityGlobalSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Publication
        fields = ("id", "title", "created_at", "tags", "community", "type")


class RecentPublicationSerializer(serializers.ModelSerializer):
    publication = PublicationForRecentSerializer()

    class Meta:
        model = RecentPublication
        exclude = ("created_by",)
