import metadata_parser
from rest_framework import serializers

from bookmark.models import Bookmark
from bookmark.serializers import BookmarkSerializer
from comment.models import Comment
from comment.serializers import CommentSerializer
from community.models import CommunityHashtag
from globals import CommunityGlobalSerializer, UserGlobalSerializer
from hide.models import Hide
from hide.serializers import HideSerializer
from publication.models import *
from share.models import Share
from share.serializers import ShareSerializer
from vote.models import Vote
from vote.serializers import VoteSerializer


class PublicationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationImage
        exclude = ["publication"]

    def create(self, validated_data):
        validated_data["publication"] = self.context["publication"]
        return super().create(validated_data)


class PublicationLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationLink
        exclude = ["publication"]

    def create(self, validated_data):
        validated_data["publication"] = self.context["publication"]
        page = metadata_parser.MetadataParser(url=validated_data.get("link"))
        image = page.get_metadata_link("image", allow_encoded_uri=True)
        page_title = page.get_metadatas(
            "title",
            strategy=[
                "page",
                "og",
                "dc",
            ],
        )
        page_desc = page.get_metadatas(
            "description",
            strategy=[
                "page",
                "og",
                "dc",
            ],
        )
        validated_data["image"] = image
        validated_data["title"] = page_title[0] if page_title else None
        validated_data["description"] = page_desc[0] if page_desc else None
        return super().create(validated_data)

    def update(self, instance, validated_data):
        page = metadata_parser.MetadataParser(url=validated_data.get("link"))
        image = page.get_metadata_link("image", allow_encoded_uri=True)
        page_title = page.get_metadatas(
            "title",
            strategy=[
                "page",
                "og",
                "dc",
            ],
        )
        page_desc = page.get_metadatas(
            "description",
            strategy=[
                "page",
                "og",
                "dc",
            ],
        )
        validated_data["image"] = image
        validated_data["title"] = page_title[0] if page_title else None
        validated_data["description"] = page_desc[0] if page_desc else None
        return super().update(instance, validated_data)


class PublicationImageUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationImageUrl
        exclude = ["publication"]

    def create(self, validated_data):
        validated_data["publication"] = self.context["publication"]
        return super().create(validated_data)


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
    up_vote = serializers.SerializerMethodField()
    down_vote = serializers.SerializerMethodField()
    share_status = serializers.SerializerMethodField()
    hidden_status = serializers.SerializerMethodField()
    bookmark_status = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    link = PublicationLinkSerializer(read_only=True)
    images = PublicationImageSerializer(read_only=True, many=True)
    image_urls = PublicationImageUrlSerializer(read_only=True, many=True)
    created_by = UserGlobalSerializer(read_only=True)

    def get_up_vote(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model():
            return False
        try:
            up_vote = Vote.objects.get(created_by=user, publication=obj, up=True)
            return VoteSerializer(up_vote).data
        except Vote.DoesNotExist:
            return False

    def get_down_vote(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model():
            return False
        try:
            down_vote = Vote.objects.get(created_by=user, publication=obj, up=False)
            return VoteSerializer(down_vote).data
        except Vote.DoesNotExist:
            return False

    def get_share_status(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model():
            return False
        try:
            share = Share.objects.get(created_by=user, publication=obj)
            return ShareSerializer(share).data
        except Share.DoesNotExist:
            return False

    def get_hidden_status(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model():
            return False
        try:
            instance = Hide.objects.get(created_by=user, publication=obj)
            return HideSerializer(instance).data
        except Hide.DoesNotExist:
            return False

    def get_bookmark_status(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model():
            return False
        try:
            bookmark = Bookmark.objects.get(created_by=user, publication=obj)
            return BookmarkSerializer(bookmark).data
        except Bookmark.DoesNotExist:
            return False

    def get_comments(self, obj):
        context = {"user": self.context["user"]}
        comments = Comment.objects.filter(publication=obj, reply=None)
        return CommentSerializer(
            comments, read_only=True, many=True, context=context
        ).data

    class Meta:
        model = Publication
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = self.context.get("depth", 0)


class TwitterOEmbedData:
    def __init__(self, source, oembed):
        self.source = source
        self.oembed = oembed


class TwitterEmbedSerializer(serializers.Serializer):
    source = serializers.URLField()
    oembed = serializers.JSONField()
