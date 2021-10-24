from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
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


class ReportAUser(APIView):
    @staticmethod
    def post(request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        report, created = ReportUser.objects.get_or_create(to_report=user, user=request.user)
        if created:
            return Response(status=status.HTTP_201_CREATED)
        return Response({"details": "Cannot report already reported user."}, status=status.HTTP_403_FORBIDDEN)


class BlockAUser(APIView):
    @staticmethod
    def post(request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        block, created = BlockUser.objects.get_or_create(to_block=user, user=request.user)
        if created:
            return Response(status=status.HTTP_201_CREATED)
        return Response({"details": "Cannot block already blocked user."}, status=status.HTTP_403_FORBIDDEN)


class UnBlockAUser(APIView):
    @staticmethod
    def delete(request, pk):
        block = get_object_or_404(BlockUser, pk=pk)
        if not block.user == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        block.delete()
        return Response(status=status.HTTP_200_OK)


class DeleteReport(APIView):
    @staticmethod
    def delete(request, pk):
        report = get_object_or_404(ReportUser, pk=pk)
        # either report creator can delete
        if not report.user == request.user:
            # or the superuser can delete it
            if not request.user.is_superuser:
                return Response(status=status.HTTP_403_FORBIDDEN)
        report.delete()
        return Response(status=status.HTTP_200_OK)
