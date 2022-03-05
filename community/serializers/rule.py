from rest_framework import serializers

from community.sub_models.rule import Rule


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        exclude = ["community"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["community"] = self.context["community"]
        return super().create(validated_data)
