from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from notification.models import Notification, NotificationTo
from notification.serializers import NotificationSerializer, NotificationToSerializer


# @receiver(post_save, sender=Notification)
# def broadcast_notifications(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         serializer = NotificationSerializer(instance, read_only=True)
#         to_serializer = NotificationToSerializer(NotificationTo.objects.filter(notification=instance), many=True)
#         print(serializer.data)
#         async_to_sync(channel_layer.group_send)(
#             "broadcast", {
#                 "type": "broadcast.notification",
#                 "event": "New Notification",
#                 "notification": serializer.data,
#                 "to": to_serializer.data
#             }
#         )
