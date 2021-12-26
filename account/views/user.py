from rest_framework import status, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import helper
from account.permissions import IsOwner
from account.serializers.user import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by("-date_joined")
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        if self.action in ["list", "delete"]:
            return UserSerializer
        elif self.action == "retrieve":
            return UserRetrieveSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return UserPostSerializer


class ProfileListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    filterset_fields = []
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


class ReportAUser(APIView):
    @staticmethod
    def post(request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        report, created = ReportUser.objects.get_or_create(
            to_report=user, user=request.user
        )
        if created:
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Cannot report already reported user."},
            status=status.HTTP_403_FORBIDDEN,
        )


class BlockAUser(APIView):
    @staticmethod
    def post(request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        block, created = BlockUser.objects.get_or_create(
            user=user, created_by=request.user
        )
        if created:
            code = status.HTTP_201_CREATED
        else:
            code = status.HTTP_200_OK
        return Response(status=code)


class UnBlockAUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        block = get_object_or_404(BlockUser, pk=pk)
        self.check_object_permissions(request, block)
        block.delete()
        return Response(status=status.HTTP_200_OK)


class DeleteReport(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        report = get_object_or_404(ReportUser, pk=pk)
        self.check_object_permissions(request, report)
        report.delete()
        return Response(status=status.HTTP_200_OK)


class MentionList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        users = get_user_model().objects.all()
        serializer = MentionUserSerializer(users, many=True, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
