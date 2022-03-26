from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from notification.models import NotificationTo
from notification.serializers import NotificationSerializer, NotificationToSerializer


@receiver(post_save, sender=NotificationTo)
def broadcast_notifications(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        serializer = NotificationSerializer(instance.notification, read_only=True)
        # Trigger message sent to group
        print("fromSignal", instance.user.username)
        async_to_sync(channel_layer.group_send)(
            # name of the channels group
            str(instance.user.username),
            {
                "type": "notify",
                "data": serializer.data,
            },
        )
