from rest_framework import serializers

from hide.models import Hide


class HideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hide
        fields = "__all__"


class MyHideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hide
        exclude = ["created_by"]
