from rest_framework import serializers

from globals import (
    UserGlobalSerializer,
    CommunityGlobalSerializer,
    PublicationGlobalSerializer,
    CommentGlobalSerializer,
)
from share.models import Share


class MyShareSerializer(serializers.ModelSerializer):
    user = UserGlobalSerializer(allow_null=True)
    community = CommunityGlobalSerializer(allow_null=True)
    publication = PublicationGlobalSerializer(allow_null=True)
    comment = CommentGlobalSerializer(allow_null=True)

    class Meta:
        model = Share
        exclude = ("created_by",)


class ShareViewSerializer(serializers.ModelSerializer):
    user = UserGlobalSerializer(allow_null=True)
    community = CommunityGlobalSerializer(allow_null=True)
    publication = PublicationGlobalSerializer(allow_null=True)
    comment = CommentGlobalSerializer(allow_null=True)
    created_by = UserGlobalSerializer(allow_null=True)

    class Meta:
        model = Share
        fields = "__all__"


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = "__all__"

    def create(self, validated_data):
        publication = self.context["publication"]
        comment = self.context["comment"]
        requestor = self.context["request"].user
        if publication:
            validated_data["publication"] = publication
        else:
            validated_data["comment"] = comment
        validated_data["created_by"] = requestor
        return super().create(validated_data)
