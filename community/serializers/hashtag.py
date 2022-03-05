from rest_framework import serializers

from community.models import Community


class PostCommunityHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ["tags"]
