from rest_framework import serializers

from globals import CommentGlobalSerializer, PublicationGlobalSerializer
from hide.models import Hide


class HideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hide
        fields = "__all__"


class MyHideSerializer(serializers.ModelSerializer):
    publication = PublicationGlobalSerializer(allow_null=True)
    comment = CommentGlobalSerializer(allow_null=True)

    class Meta:
        model = Hide
        exclude = ["created_by"]
