from rest_framework import serializers

from choices import RESOLVE_REPORT_STATES
from report.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"

    def create(self, validated_data):
        context = self.context
        if context["user"]:
            validated_data["user"] = context["user"]
        elif context["community"]:
            validated_data["community"] = context["community"]
        elif context["publication"]:
            validated_data["publication"] = context["publication"]
        elif context["comment"]:
            validated_data["comment"] = context["comment"]
        elif context["share"]:
            validated_data["share"] = context["share"]
        validated_data["created_by"] = context["request"].user
        return super().create(validated_data)


class ResolveReportSerializer(serializers.Serializer):
    resolve_text = serializers.CharField(max_length=1000, required=True)
    status = serializers.ChoiceField(required=True, choices=RESOLVE_REPORT_STATES)
