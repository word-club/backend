from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsOwner
from comment.models import Comment
from image.models import Image
from image.serializers import (
    CommentImageSerializer,
    ImageSerializer,
    PublicationImageSerializer,
)
from publication.models import Publication


class AddPublicationImageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        context = {"publication": publication, "request": request}
        serializer = PublicationImageSerializer(data=request.data, context=context)
        if serializer.is_valid():
            try:
                serializer.save()
            except ValidationError as e:
                return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommentImageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        context = {"comment": comment, "request": request}
        serializer = CommentImageSerializer(data=request.data, context=context)
        if serializer.is_valid():
            try:
                serializer.save()
            except ValidationError as e:
                return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, pk):
        image = get_object_or_404(Image, pk=pk)
        self.check_object_permissions(request, image)
        serializer = ImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        image = get_object_or_404(Image, pk=pk)
        self.check_object_permissions(request, image)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
