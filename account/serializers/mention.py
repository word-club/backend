from collections import OrderedDict

from django.contrib.auth import get_user_model

from rest_framework import serializers

from helpers.get_active import get_active_avatar_for


class MentionUserSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    @staticmethod
    def get_display_name(obj):
        return obj.profile.display_name

    @staticmethod
    def get_avatar(obj):
        filterset = OrderedDict()
        filterset["profile"] = obj.profile
        return get_active_avatar_for(filterset)

    class Meta:
        model = get_user_model()
        fields = ["id", "display_name", "username", "avatar"]
