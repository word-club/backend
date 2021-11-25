from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import FollowUser
from account.permissions import IsOwner
from account.serializers.follow import FollowUserSerializer


class FollowUserViewSet(
    mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = FollowUser.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = FollowUserSerializer
    filterset_fields = ["user", "created_by"]

    def get_permissions(self):
        return [IsOwner] if self.action == "delete" else [IsAuthenticated]


class FollowAUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        to_follow = get_object_or_404(get_user_model(), pk=pk)
        follow = FollowUser.objects.create(user=to_follow, created_by=request.user)
        return Response(
            FollowUserSerializer(follow).data,
            status=status.HTTP_201_CREATED
        )


class UnFollowAUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        instance = get_object_or_404(FollowUser, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response(status=status.HTTP_200_OK)
