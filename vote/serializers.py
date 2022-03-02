from rest_framework import serializers

from vote.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        exclude = ["comment", "publication", "up"]
