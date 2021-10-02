from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from notification.permissions import IsNotificationReceiver
from notification.serializers import *


class NotificationListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(
            instance=notifications, many=True, read_only=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        serializer = NotificationPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestroyNotificationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SetANotificationAsSeen(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsNotificationReceiver]

    def post(self, request, pk):
        notification_to = get_object_or_404(NotificationTo, pk=pk)
        self.check_object_permissions(request, notification_to)
        if notification_to.seen: return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            notification_to.seen = True
            notification_to.save()
            return Response(status=status.HTTP_200_OK)
