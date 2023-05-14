from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsOwner, IsSuperUser
from comment.models import Comment
from publication.models import Publication
from publication.permissions import IsPublished
from share.models import Share
from share.serializers import ShareSerializer, ShareViewSerializer


class AddPublicationShare(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsPublished]

    def post(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        context = {"publication": publication, "request": request, "comment": None}
        serializer = ShareSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommentShare(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsPublished]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment.publication)
        context = {"comment": comment, "request": request, "publication": None}
        serializer = ShareSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, pk):
        share = get_object_or_404(Share, pk=pk)
        self.check_object_permissions(request, share)
        serializer = ShareSerializer(share)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        share = get_object_or_404(Share, pk=pk)
        self.check_object_permissions(request, share)
        serializer = ShareSerializer(share, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        share = get_object_or_404(Share, pk=pk)
        self.check_object_permissions(request, share)
        share.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShareList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request):
        self.check_object_permissions(request, request.user)
        shares = Share.objects.all()
        serializer = ShareViewSerializer(shares, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
