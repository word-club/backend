from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers.user import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by("-date_joined")
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        if self.action in ["list", "delete"]:
            return UserSerializer
        elif self.action == "retrieve":
            return UserInfoSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return UserPostSerializer


class RegisterUserView(APIView):
    @staticmethod
    def post(request):
        serializer = UserPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
