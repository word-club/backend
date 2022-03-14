from rest_framework import serializers

from globals import CommentGlobalSerializer, PublicationGlobalSerializer
from vote.models import Vote


class VoteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        exclude = ["comment", "publication", "up"]


class MyVoteSerializer(serializers.ModelSerializer):
    publication = PublicationGlobalSerializer(allow_null=True)
    comment = CommentGlobalSerializer(allow_null=True)

    class Meta:
        model = Vote
        exclude = [
            "created_by",
        ]
