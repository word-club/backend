from django.contrib.auth import get_user_model

from rest_framework import serializers

from avatar.models import Avatar


class MentionUserSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    @staticmethod
    def get_username(obj):
        return obj.username

    @staticmethod
    def get_display_name(obj):
        return obj.profile.display_name

    @staticmethod
    def get_avatar(obj):
        try:
            avatar = Avatar.objects.get(profile__user=obj, is_active=True)
            return avatar.image.url
        except Avatar.DoesNotExist:
            return None

    class Meta:
        model = get_user_model()
        fields = ["id", "display_name", "username", "avatar"]
