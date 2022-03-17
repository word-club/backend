from rest_framework import serializers

from choices import RESOLVE_REPORT_STATES
from globals import (
    UserGlobalSerializer,
    PublicationGlobalSerializer,
    CommentGlobalSerializer,
    CommunityGlobalSerializer,
    ShareGlobalSerializer,
)
from report.models import Report


class ReportSerializer(serializers.ModelSerializer):
    created_by = UserGlobalSerializer(read_only=True)
    resolved_by = UserGlobalSerializer(read_only=True)

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


class MyReportSerializer(serializers.ModelSerializer):
    user = UserGlobalSerializer(allow_null=True)
    publication = PublicationGlobalSerializer(allow_null=True)
    comment = CommentGlobalSerializer(allow_null=True)
    community = CommunityGlobalSerializer(allow_null=True)
    share = ShareGlobalSerializer(allow_null=True)

    class Meta:
        model = Report
        exclude = ("created_by",)
