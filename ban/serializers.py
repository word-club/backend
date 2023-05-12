from django.apps import apps
from rest_framework import serializers

from ban.models import Ban


class CreateBanSerializer(serializers.ModelSerializer):
    def validate(self, data):
        print(apps.get_model(
            app_label=data["ban_item_app_label"], model_name=data["ban_item_model"]
        ).objects.filter(id=data["ban_item_id"]).exists())
        if apps.get_model(
            app_label=data["ban_item_app_label"], model_name=data["ban_item_model"]
        ).objects.filter(id=data["ban_item_id"]).exists():
            return data
        raise serializers.ValidationError({
            "ban_item_id": "The ban item does not exist."
        })

    class Meta:
        model = Ban
        fields = "__all__"
