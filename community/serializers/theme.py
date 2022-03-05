from rest_framework import serializers

from community.sub_models.theme import Theme


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        exclude = ["community"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().update(instance, validated_data)
