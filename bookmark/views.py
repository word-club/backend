from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsOwner, IsSuperUser
from bookmark.models import Bookmark
from bookmark.serializers import BookmarkSerializer, BookmarkViewSerializer
from comment.models import Comment
from community.models import Community
from publication.models import Publication


class AddPublicationBookmark(APIView):
    """
    Add a bookmark to a publication
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        _, created = Bookmark.objects.get_or_create(
            publication=publication, created_by=request.user
        )
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class AddCommunityBookmark(APIView):
    """
    Add a bookmark to a community
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        community = get_object_or_404(Community, pk=pk)
        _, created = Bookmark.objects.get_or_create(community=community, created_by=request.user)
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class AddCommentBookmark(APIView):
    """
    Add a bookmark to a comment
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        _, created = Bookmark.objects.get_or_create(comment=comment, created_by=request.user)
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(status=http_status)


class BookmarkDetail(APIView):
    """
    Retrieve or delete a bookmark instance.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    @staticmethod
    def get(request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk)
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk)
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookmarkList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request):
        self.check_object_permissions(request, request.user)
        bookmarks = Bookmark.objects.all()
        serializer = BookmarkViewSerializer(bookmarks, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

