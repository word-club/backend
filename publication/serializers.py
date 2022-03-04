from rest_framework import serializers

from comment.models import Comment
from comment.serializers import CommentSerializer
from community.models import CommunityHashtag
from globals import CommunityGlobalSerializer, UserGlobalSerializer
from image.serializers import PublicationImageSerializer
from link.serializers import LinkInfoSerializer
from publication.models import *
from share.models import Share
from vote.models import Vote


class PublicationHashtags(serializers.ModelSerializer):
    hashtag = serializers.SerializerMethodField()

    @staticmethod
    def get_hashtag(obj):
        return {"id": obj.hashtag.id, "tag": obj.hashtag.tag}

    class Meta:
        model = PublicationHashtag
        exclude = ["publication"]


class PublicationFormSerializer(serializers.ModelSerializer):
    hash_tags = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Hashtag.objects.all()),
        max_length=2,
        required=False,
        allow_null=True,
        write_only=True,
    )

    class Meta:
        model = Publication
        fields = "__all__"

    def validate(self, validated_data):
        tag_not_found = []
        hashtags = validated_data.get("hash_tags")
        community = validated_data.get("community")
        if hashtags and community:
            for hashtag in hashtags:
                try:
                    CommunityHashtag.objects.get(tag=hashtag, community=community)
                except CommunityHashtag.DoesNotExist:
                    tag_not_found.append(
                        {"tag": hashtag.tag, "id": hashtag.id, "detail": "Not allowed."}
                    )
                    raise serializers.ValidationError({"hash_tags": tag_not_found})
        return validated_data

    def create(self, validated_data):
        validated_data["created_by"] = self.context["user"]
        hashtags = None
        if validated_data.get("hash_tags"):
            hashtags = validated_data.pop("hash_tags")
        publication = Publication.objects.create(**validated_data)
        if hashtags:
            for hashtag in hashtags:
                PublicationHashtag.objects.create(
                    hashtag=hashtag, publication=publication
                )
        return publication

    def update(self, instance, validated_data):
        hashtags = None
        if validated_data.get("hash_tags"):
            hashtags = validated_data.pop("hash_tags")
        if hashtags:
            for hashtag in hashtags:
                PublicationHashtag.objects.get_or_create(
                    hashtag=hashtag, publication=instance
                )
        return super().update(instance, validated_data)


def get_publication_reactions(publication):
    up_votes = Vote.objects.filter(publication=publication, up=True).count()
    down_votes = Vote.objects.filter(publication=publication, up=False).count()
    shares = Share.objects.filter(publication=publication).count()
    comments = Comment.objects.filter(publication=publication).count()
    total = up_votes + down_votes + shares + comments

    return {
        "up_votes": up_votes,
        "down_votes": down_votes,
        "shares": shares,
        "comments": comments,
        "total": total,
    }


class PublicationSerializer(serializers.ModelSerializer):
    community = CommunityGlobalSerializer()
    hashtags = PublicationHashtags(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    links = LinkInfoSerializer(read_only=True)
    images = PublicationImageSerializer(read_only=True, many=True)
    created_by = UserGlobalSerializer(read_only=True)

    class Meta:
        model = Publication
        fields = "__all__"
