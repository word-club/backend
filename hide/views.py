from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsOwner
from comment.models import Comment
from community.models import Community
from hide.models import Hide
from hide.serializers import HideSerializer
from publication.models import Publication


class HideAPublication(APIView):
    """
    Hide a publication
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk):
        user = request.user
        publication = get_object_or_404(Publication, pk=pk)
        _, created = Hide.objects.get_or_create(
            created_by=user, publication=publication
        )
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class HideAComment(APIView):
    """
    Hide a comment
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk):
        user = request.user
        comment = get_object_or_404(Comment, pk=pk)
        _, created = Hide.objects.get_or_create(created_by=user, comment=comment)
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class HideACommunity(APIView):
    """
    Hide a community
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk):
        user = request.user
        community = get_object_or_404(Community, pk=pk)
        _, created = Hide.objects.get_or_create(created_by=user, community=community)
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class HideAUser(APIView):
    """
    Hide a user
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk):
        requestor = request.user
        user = get_object_or_404(get_user_model(), pk=pk)
        _, created = Hide.objects.get_or_create(created_by=requestor, user=user)
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class HideDetail(APIView):
    """
    Hide detail
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner, IsAdminUser)

    def get(self, request, pk):
        hide = get_object_or_404(Hide, pk=pk)
        self.check_object_permissions(request, hide)
        serializer = HideSerializer(hide)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        hide = get_object_or_404(Hide, pk=pk)
        self.check_object_permissions(request, hide)
        hide.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
