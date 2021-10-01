from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsOwner
from comment.serializers import *
from publication.permissions import IsPublicationAuthor


class AddPublicationComment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        context = {"publication": publication, "request": request}
        serializer = CommentPostSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDestroyCommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner, IsPublicationAuthor]

    def patch(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        comment_images = CommentImage.objects.filter(comment=comment)
        [img.image.delete() for img in comment_images]
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpVoteACommentView(APIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        up_vote, created = CommentUpVote.objects.get_or_create(
            created_by=request.user,
            comment=comment
        )
        if created: Response(status=status.HTTP_201_CREATED)
        else: Response(status=status.HTTP_200_OK)


class DownVoteACommentView(APIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        down_vote, created = CommentDownVote.objects.get_or_create(
            created_by=request.user,
            comment=comment
        )
        if created: Response(status=status.HTTP_201_CREATED)
        else: Response(status=status.HTTP_200_OK)


class ReportACommentView(APIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        reports = ReportComment.objects.filter(created_by=request.user, comment=comment)
        most_recent_report_found, diff = helper.is_recent_report_present(reports)

        if most_recent_report_found: return Response(
            data={"details": "recently reported", "remaining": 15 - diff},
            status=status.HTTP_403_FORBIDDEN
        )

        context = {"comment": comment, "request": request}
        serializer = CommentReportSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCommentReportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        report = get_object_or_404(ReportComment, pk=pk)
        self.check_object_permissions(request, report)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveCommentImageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        comment_image = get_object_or_404(CommentImage, pk=pk)
        self.check_object_permissions(request, comment_image.comment)
        comment_image.image.delete()
        comment_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveCommentImageUrlView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        comment_image_url = get_object_or_404(CommentImageUrl, pk=pk)
        self.check_object_permissions(request, comment_image_url.comment)
        comment_image_url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveCommentVideoUrlView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        comment_video_url = get_object_or_404(CommentVideoUrl, pk=pk)
        self.check_object_permissions(request, comment_video_url.comment)
        comment_video_url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveUpVoteForACommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        up_vote = get_object_or_404(CommentUpVote, pk=pk)
        self.check_object_permissions(request, up_vote)
        up_vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveDownVoteForACommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        down_vote = get_object_or_404(CommentDownVote, pk=pk)
        self.check_object_permissions(request, down_vote)
        down_vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
