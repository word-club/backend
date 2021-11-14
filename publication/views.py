from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

import helper
from account.permissions import IsOwner
from community.models import CommunitySubscription
from community.permissions import IsCommunityAdministrator, IsSubscriber
from publication.serializers import *


class PublicationListRetrieveView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    authentication_classes = []
    permission_classes = []
    filterset_fields = ["created_by", "is_published", "timestamp", "type"]
    search_fields = ["title", "content"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        depth = 0
        try:
            depth = int(self.request.query_params.get("depth", 0))
        # Ignore non-numeric parameters and keep default 0 depth
        except ValueError:
            pass
        context["depth"] = depth
        return context


def check_community_law(community, user):
    if community:
        try:
            subscriber = CommunitySubscription.objects.get(subscriber=user)
            if subscriber.is_banned:
                return True, {
                    "detail": "Subscriber is banned for the selected community."
                }
            if community.type != "public":
                if not subscriber.is_approved:
                    return True, {"detail": "Subscriber is not approved yet."}
        except CommunitySubscription.DoesNotExist:
            return True, {
                "detail": "Please subscribe the community first to add publication."
            }


class AddPublicationView(APIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request):
        context = {"request": request}
        serializer = PublicationSerializer(data=request.data, context=context)
        if serializer.is_valid():
            community = serializer.validated_data.get("community")
            if community:
                do_break, detail = check_community_law(community, request.user)
                if do_break:
                    return Response(detail, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePublicationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner | IsCommunityAdministrator]

    def patch(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        serializer = PublicationSerializer(publication, data=request.data, partial=True)
        if serializer.is_valid():
            community = serializer.validated_data.get("community")
            if community:
                do_break, detail = check_community_law(community, request.user)
                if do_break:
                    return Response(detail, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        publication.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublishPublicationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def post(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        if publication.is_published:
            return Response(
                {"detail": "Publication already published."},
                status=status.HTTP_204_NO_CONTENT,
            )
        if not publication.title:
            return Response(
                {"title": "This field is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        if publication.type is 'editor' and not publication.content:
            return Response(
                {"content": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if publication.community:
            do_break, detail = check_community_law(publication.community, request.user)
            if do_break:
                return Response(detail, status=status.HTTP_403_FORBIDDEN)
        publication.is_published = True
        publication.published_at = timezone.now()
        publication.save()
        return Response(PublicationSerializer(publication).data, status=status.HTTP_200_OK)


class AddPublicationImageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def post(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        context = {"publication": publication, "request": request}
        serializer = PublicationImageSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemovePublicationImageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        publication_image = get_object_or_404(PublicationImage, pk=pk)
        self.check_object_permissions(request, publication_image.publication)
        publication_image.image.delete()
        publication_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddPublicationImageUrlView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def post(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        context = {"publication": publication, "request": request}
        serializer = PublicationImageUrlSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemovePublicationImageUrlView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        img_url = get_object_or_404(PublicationImageUrl, pk=pk)
        self.check_object_permissions(request, img_url.publication)
        img_url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpVoteAPublicationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        up_vote, created = PublicationUpVote.objects.get_or_create(
            created_by=request.user, publication=publication
        )
        if created:
            Response(status=status.HTTP_201_CREATED)
        else:
            Response(status=status.HTTP_200_OK)


class RemovePublicationUpVote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        up_vote = get_object_or_404(PublicationUpVote, pk=pk)
        self.check_object_permissions(request, up_vote)
        up_vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownVoteAPublication(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        down_vote, created = PublicationDownVote.objects.get_or_create(
            created_by=request.user, publication=publication
        )
        if created:
            Response(status=status.HTTP_201_CREATED)
        else:
            Response(status=status.HTTP_200_OK)


class RemovePublicationDownVote(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        down_vote = get_object_or_404(PublicationDownVote, pk=pk)
        self.check_object_permissions(request, down_vote)
        down_vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookmarkAPublicationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        bookmark, created = PublicationBookmark.objects.get_or_create(
            created_by=request.user, publication=publication
        )
        if created:
            Response(status=status.HTTP_201_CREATED)
        else:
            Response(status=status.HTTP_200_OK)


class RemovePublicationBookmarkView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        bookmark = get_object_or_404(PublicationDownVote, pk=pk)
        self.check_object_permissions(request, bookmark)
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HideAPublicationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        up_vote, created = HidePublication.objects.get_or_create(
            created_by=request.user, publication=publication
        )
        if created:
            Response(status=status.HTTP_201_CREATED)
        else:
            Response(status=status.HTTP_200_OK)


class RemovePublicationHiddenStateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        hidden_pub = get_object_or_404(HidePublication, pk=pk)
        self.check_object_permissions(request, hidden_pub)
        hidden_pub.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportAPublicationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        reports = ReportPublication.objects.filter(
            created_by=request.user, publication=publication
        )
        most_recent_report_found, diff = helper.is_recent_report_present(reports)

        if most_recent_report_found:
            return Response(
                data={"detail": "recently reported", "remaining": 15 - diff},
                status=status.HTTP_403_FORBIDDEN,
            )

        context = {"publication": publication, "request": request}
        serializer = PublicationReportSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemovePublicationReportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        report = get_object_or_404(ReportPublication, pk=pk)
        self.check_object_permissions(request, report)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddPublicationLinkView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def post(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        context = {"publication": publication}
        serializer = PublicationLinkSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditOrRemovePublicationLink(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def patch(self, request, pk):
        publication_link = get_object_or_404(PublicationLink, pk=pk)
        self.check_object_permissions(request, publication_link.publication)
        serializer = PublicationLinkSerializer(publication_link, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        publication_link = get_object_or_404(PublicationLink, pk=pk)
        self.check_object_permissions(request, publication_link.publication)
        publication_link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
