from django.utils import timezone

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


def check_publication_update_date_limit(obj):
    """
    :param obj: Publication instance
    :return: void if publication is not published yet
        Response(403) if publication update date limit reached
    """
    now = timezone.now()
    if not obj.published_at:
        return
    diff = now - obj.published_at
    limit = Administration.objects.first()
    if diff.days > limit.publication_update_limit:
        return Response(
            {
                "detail": "Sorry, you cannot update the publication after {} days.".format(
                    limit.publication_update_limit
                )
            },
            status=status.HTTP_403_FORBIDDEN,
        )


class PublicationListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PublicationSerializer
    authentication_classes = []
    permission_classes = []
    filterset_fields = [
        "created_by",
        "is_published",
        "timestamp",
        "type",
        "community",
        "is_pinned",
    ]

    def get_queryset(self):
        filterset, sort_string = helper.get_viewset_filterset(
            self.request, self.filterset_fields, "published_at"
        )
        return Publication.objects.filter(**filterset).order_by(sort_string)

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
        if request.user != publication.created_by:
            publication.views += 1
            publication.save()
        context = {"user": request.user, "depth": 2}
        return Response(
            PublicationSerializer(publication, context=context).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        context = {"user": request.user}
        publication = get_object_or_404(Publication, pk=pk)
        check_publication_update_date_limit(publication)
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
            publication = serializer.save()
            return Response(
                PublicationSerializer(publication, context=context).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        publication.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublishPublicationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner | IsCommunityAdministrator]

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
        bookmark = get_object_or_404(PublicationBookmark, pk=pk)
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


class PublicationPinView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner | IsCommunityAdministrator]

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


class ViewAPublication(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request, pk=None):
        publication = get_object_or_404(Publication, pk=pk)
        publication.views += 1
        publication.save()
        context = {"user": request.user}
        serializer = PublicationSerializer(publication, read_only=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)
