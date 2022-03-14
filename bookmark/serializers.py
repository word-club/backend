from rest_framework import serializers

from bookmark.models import Bookmark
from globals import PublicationGlobalSerializer, CommentGlobalSerializer, CommunityGlobalSerializer


class MyBookmarkSerializer(serializers.ModelSerializer):
    community = CommunityGlobalSerializer(allow_null=True)
    comment = CommentGlobalSerializer(allow_null=True)
    publication = PublicationGlobalSerializer(allow_null=True)

    class Meta:
        model = Bookmark
        exclude = ["created_by"]


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"
