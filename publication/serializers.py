import metadata_parser
from rest_framework import serializers

from comment.models import Comment
from comment.serializers import CommentSerializer
from globals import CommunityGlobalSerializer, UserGlobalSerializer
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


class PublicationShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationShare
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["publication"] = self.context["publication"]
        return super().create(validated_data)


class HidePublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HidePublication
        fields = "__all__"


class PublicationBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationBookmark
        fields = "__all__"


class PublicationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["user"]
        return super().create(validated_data)


class PublicationSerializer(serializers.ModelSerializer):
    community = CommunityGlobalSerializer()
    reactions = serializers.SerializerMethodField()
    up_vote = serializers.SerializerMethodField()
    down_vote = serializers.SerializerMethodField()
    share_status = serializers.SerializerMethodField()
    hidden_status = serializers.SerializerMethodField()
    bookmark_status = serializers.SerializerMethodField()
    comments = CommentSerializer(read_only=True, many=True)
    link = PublicationLinkSerializer(read_only=True)
    images = PublicationImageSerializer(read_only=True, many=True)
    image_urls = PublicationImageUrlSerializer(read_only=True, many=True)
    created_by = UserGlobalSerializer(read_only=True)

    @staticmethod
    def get_reactions(obj):
        up_votes = PublicationUpVote.objects.filter(publication=obj).count()
        down_votes = PublicationDownVote.objects.filter(publication=obj).count()
        shares = PublicationShare.objects.filter(publication=obj).count()
        comments = Comment.objects.filter(publication=obj).count()
        total =  up_votes + down_votes + shares + comments

        return {
            "up_votes": up_votes,
            "down_votes": down_votes,
            "shares": shares,
            "comments": comments,
            "total": total
        }

    def get_up_vote(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            up_vote = PublicationUpVote.objects.get(created_by=user, publication=obj)
            return PublicationUpVoteSerializer(up_vote).data
        except PublicationUpVote.DoesNotExist:
            return False

    def get_down_vote(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            down_vote = PublicationDownVote.objects.get(created_by=user, publication=obj)
            return PublicationDownVoteSerializer(down_vote).data
        except PublicationDownVote.DoesNotExist:
            return False

    def get_share_status(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            share = PublicationShare.objects.get(created_by=user, publication=obj)
            return PublicationShareSerializer(share).data
        except PublicationShare.DoesNotExist:
            return False

    def get_hidden_status(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            instance = HidePublication.objects.get(created_by=user, publication=obj)
            return HidePublicationSerializer(instance).data
        except HidePublication.DoesNotExist:
            return False

    def get_bookmark_status(self, obj):
        user = self.context["user"]
        if type(user) != get_user_model(): return False
        try:
            bookmark = PublicationBookmark.objects.get(created_by=user, publication=obj)
            return PublicationBookmarkSerializer(bookmark).data
        except PublicationBookmark.DoesNotExist:
            return False


    class Meta:
        model = Publication
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = self.context.get("depth", 0)




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
