from rest_framework import serializers

from image.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class PublicationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ("comment", "publication")

    def create(self, validated_data):
        validated_data["publication"] = self.context["publication"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ("comment", "publication")

    def create(self, validated_data):
        validated_data["comment"] = self.context["comment"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
