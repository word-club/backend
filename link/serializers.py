import metadata_parser
from rest_framework import serializers

from link.models import Link

strategy = ["page", "og", "dc"]


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = "__all__"


class LinkInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        exclude = (
            "publication",
            "comment",
        )


class LinkPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        exclude = ["publication", "comment"]

    def create(self, validated_data):
        if self.context["publication"]:
            validated_data["publication"] = self.context["publication"]
        if self.context["comment"]:
            validated_data["comment"] = self.context["comment"]
        validated_data["created_by"] = self.context["request"].user
        page = metadata_parser.MetadataParser(url=validated_data.get("link"))
        image = page.get_metadata_link("image", allow_encoded_uri=True)
        page_title = page.get_metadatas("title", strategy=strategy)
        page_desc = page.get_metadatas("description", strategy=strategy)
        validated_data["image"] = image if image else None
        validated_data["title"] = page_title[0] if page_title else None
        validated_data["description"] = page_desc[0] if page_desc else None
        return super().create(validated_data)

    def update(self, instance, validated_data):
        page = metadata_parser.MetadataParser(url=validated_data.get("link"))
        image = page.get_metadata_link("image", allow_encoded_uri=True)
        page_title = page.get_metadatas("title", strategy=strategy)
        page_desc = page.get_metadatas("description", strategy=strategy)
        validated_data["image"] = image if image else None
        validated_data["title"] = page_title[0] if page_title else None
        validated_data["description"] = page_desc[0] if page_desc else None
        return super().update(instance, validated_data)
