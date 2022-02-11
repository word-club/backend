from rest_framework import serializers
from notification.models import *


class NotificationToSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTo
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    receivers = NotificationToSerializer(many=True, read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"


class NotificationReceiverSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(read_only=True)

    class Meta:
        model = NotificationTo
        fields = "__all__"
