from rest_framework import serializers

from hide.models import Hide


class HideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hide
        fields = "__all__"
