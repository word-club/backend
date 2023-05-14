from rest_framework import serializers

from ban.serializers import BanSerializer
from comment.models import Comment
from comment.serializers import CommentSerializer
from globals import CommunityGlobalSerializer, UserGlobalSerializer, PublicationGlobalSerializer
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

    def get_comments(self, obj):
        # only include comment items that are not replies
        # replies are included in the parent comment
        comments = Comment.objects.filter(publication=obj, reply=None)
        return CommentSerializer(comments, many=True, context=self.context).data

    class Meta:
        model = Publication
        fields = "__all__"


class MyPublicationSerializer(serializers.ModelSerializer):
    community = CommunityGlobalSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    links = LinkInfoSerializer(read_only=True)
    images = PublicationImageSerializer(read_only=True, many=True)
    tags = HashtagSerializer(read_only=True, many=True)

    ban = serializers.SerializerMethodField()

    @staticmethod
    def get_ban(obj):
        return BanSerializer(obj.is_banned).data if obj.is_banned else None

    class Meta:
        model = Publication
        exclude = ("created_by",)


class RecentPublicationSerializer(serializers.ModelSerializer):
    publication = PublicationGlobalSerializer()

    class Meta:
        model = RecentPublication
        exclude = ("created_by",)
