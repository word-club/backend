from rest_framework import serializers

from bookmark.models import Bookmark


class MyBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        exclude = ["created_by"]


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"
