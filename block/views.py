from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsOwner
from block.models import Block
from block.serializers import BlockSerializer
from community.models import Community


class BlockACommunity(APIView):
    """
    Block a community
    """

    @staticmethod
    def post(request, pk):
        community = get_object_or_404(Community, pk=pk)
        block, created = Block.objects.get_or_create(
            community=community, created_by=request.user
        )
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class BlockAUser(APIView):
    """
    Block a user
    """

    @staticmethod
    def post(request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        block, created = Block.objects.get_or_create(user=user, created_by=request.user)
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class BlockDetail(APIView):
    """
    Block detail
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def get(self, request, pk):
        block = get_object_or_404(Block, pk=pk)
        self.check_object_permissions(request, block)
        serializer = BlockSerializer(block)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        block = get_object_or_404(Block, pk=pk)
        self.check_object_permissions(request, block)
        block.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
