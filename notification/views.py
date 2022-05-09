from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsOwner
from notification.permissions import IsNotificationReceiver
from notification.serializers import *


class MyNotificationList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        my_notifications = NotificationTo.objects.filter(user=request.user)
        unseen_count = my_notifications.filter(seen=False).count()
        serializer = MyNotificationSerializer(instance=my_notifications, many=True, read_only=True)
        return Response({
            "unseen_count": unseen_count,
            "count": my_notifications.count(),
            "results": serializer.data
        }, status=status.HTTP_200_OK)


class DestroyNotificationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    @staticmethod
    def delete(request, pk):
        notification = get_object_or_404(NotificationTo, pk=pk)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SetANotificationAsSeen(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsNotificationReceiver]

    def post(self, request, pk):
        notification_to = get_object_or_404(NotificationTo, pk=pk)
        self.check_object_permissions(request, notification_to)
        if notification_to.seen:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            notification_to.seen = True
            notification_to.save()
            return Response(status=status.HTTP_200_OK)
