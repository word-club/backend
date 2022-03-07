from rest_framework import status, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import helper
from account.serializers.user import *


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_user_model().objects.all().order_by("-date_joined")
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["list", "delete"]:
            return UserSerializer
        else:
            return UserPostSerializer


class ProfileListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    search_fields = ["first_name", "last_name", "username"]
    serializer_class = UserSerializer

    def get_queryset(self):
        filterset, sort_string = helper.get_viewset_filterset(
            self.request, self.filterset_fields, "created_at"
        )
        return Profile.objects.filter(**filterset).order_by(sort_string)


class GetMeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        me = request.user
        return Response(UserInfoSerializer(me).data, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    @staticmethod
    def post(request):
        serializer = UserPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUserByUsername(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get(request, username):
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserInfoSerializer(user, context={"user": request.user}, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
