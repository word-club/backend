from rest_framework import serializers

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
    class Meta:
        model = Vote
        exclude = [
            "created_by",
        ]
