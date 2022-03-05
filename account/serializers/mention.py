from django.contrib.auth import get_user_model

from rest_framework import serializers

from avatar.models import Avatar


class MentionUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    @staticmethod
    def get_username(obj):
        return obj.username

    @staticmethod
    def get_name(obj):
        if obj.first_name and obj.last_name:
            return "{} {}".format(obj.first_name, obj.last_name)
        return obj.username

    @staticmethod
    def get_avatar(obj):
        try:
            avatar = Avatar.objects.get(profile__user=obj, is_active=True)
            return avatar.image.url
        except Avatar.DoesNotExist:
            return None

    class Meta:
        model = get_user_model()
        fields = ["id", "name", "username", "avatar"]
