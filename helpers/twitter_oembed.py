from rest_framework import serializers


class TwitterOEmbedData:
    def __init__(self, source, oembed):
        self.source = source
        self.oembed = oembed


class TwitterEmbedSerializer(serializers.Serializer):
    source = serializers.URLField()
    oembed = serializers.JSONField()
