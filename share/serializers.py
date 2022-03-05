from rest_framework import serializers

from share.models import Share


class MyShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        exclude = ("created_by",)


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
