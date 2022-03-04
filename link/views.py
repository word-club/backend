from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from account.permissions import IsOwner
from comment.models import Comment
from link.models import Link
from publication.models import Publication
from link.serializers import LinkPostSerializer


class AddPublicationLinkView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        context = {
            "publication": publication,
            "comment": False,
            "request": request,
        }
        serializer = LinkPostSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommentLinkView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        context = {
            "publication": False,
            "comment": comment,
            "request": request,
        }
        serializer = LinkPostSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LinkDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, pk):
        link = get_object_or_404(Link, pk=pk)
        self.check_object_permissions(request, link.publication)
        serializer = LinkPostSerializer(link)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        link = get_object_or_404(Link, pk=pk)
        self.check_object_permissions(request, link.publication)
        serializer = LinkPostSerializer(link, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        link = get_object_or_404(Link, pk=pk)
        self.check_object_permissions(request, link.publication)
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
