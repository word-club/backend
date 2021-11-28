from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

import helper
from account.permissions import IsOwner
from community.helper import check_community_law
from community.permissions import IsCommunityAdministrator
from publication.serializers import *
from rest_framework.authtoken.models import Token


class PublicationListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationFormSerializer
    authentication_classes = []
    permission_classes = []
    filterset_fields = ["created_by", "is_published", "timestamp", "type", "community", "is_pinned"]
    search_fields = ["title", "content"]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        depth = 0
        try:
            depth = int(self.request.query_params.get("depth", 0))
        except ValueError:
            pass
        try:
            auth_header = self.request.headers.get("Authorization")
            if auth_header != "null" and auth_header:
                token = auth_header.split(" ")[1]
                token_instance = Token.objects.get(key=token)
                context["user"] = token_instance.user
            else:
                context["user"] = None
        except ValueError:
            pass
        context["depth"] = depth
        return context


class AddPublicationView(APIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request):
        context = {"user": request.user}
        serializer = PublicationFormSerializer(data=request.data, context=context)
        if serializer.is_valid():
            community = serializer.validated_data.get("community")
            if community:
                do_break, detail = check_community_law(community, request.user)
                if do_break:
                    return Response(detail, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdatePublicationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner | IsCommunityAdministrator]

    @staticmethod
    def get(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        context = {"user": request.user, "depth": 2}
        return Response(
            PublicationSerializer(
                publication, context=context
            ).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        serializer = PublicationFormSerializer(
            publication, data=request.data, partial=True, context={"user": request.user}
        )
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
    permission_classes = [IsOwner|IsCommunityAdministrator]

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
        if publication.type == "editor" and not publication.content:
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
        return Response(
            PublicationSerializer(publication, context={"user": request.user}).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk=None):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        if publication.is_draft():
            return Response(status=status.HTTP_200_OK)
        publication.is_published = False
        publication.published_at = None
        publication.save()
        return Response(status=status.HTTP_201_CREATED)

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
            return Response(
                PublicationSerializer(publication, context={"user": request.user}).data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


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
            return Response(
                PublicationSerializer(publication, context={"user": request.user}).data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                PublicationDownVoteSerializer(down_vote).data, status=status.HTTP_200_OK
            )


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
            return Response(
                PublicationSerializer(publication, context={"user": request.user}).data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


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
        instance, created = HidePublication.objects.get_or_create(
            created_by=request.user, publication=publication
        )
        if created:
            return Response(
                PublicationSerializer(publication, context={"user": request.user}).data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                HidePublicationSerializer(instance).data,
                status=status.HTTP_204_NO_CONTENT,
            )


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
            return Response(
                PublicationSerializer(publication, context={"user": request.user}).data,
                status=status.HTTP_201_CREATED,
            )
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


class GetTwitterEmbed(APIView):
    authentication_classes = []

    def post(self, request):
        source = request.data.get("source")
        if not source:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = TwitterEmbedSerializer(
            TwitterOEmbedData(
                source=source, oembed=helper.get_twitter_embed_data(source)
            )
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShareAPublicationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        context = {"publication": publication, "request": request}
        serializer = PublicationShareSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            publication.timestamp = timezone.now()
            publication.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveMyShareForPublication(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    @staticmethod
    def delete(request, pk):
        share = get_object_or_404(PublicationShare, pk=pk)
        share.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublicationPinView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner|IsCommunityAdministrator]

    def patch(self, request, pk=None):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        if publication.is_pinned:
            return Response(status=status.HTTP_200_OK)
        publication.is_pinned = True
        publication.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        if publication.is_pinned:
            publication.is_pinned = False
            publication.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_200_OK)
