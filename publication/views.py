from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers import helper
from account.permissions import IsOwner
from community.helper import check_community_law
from community.permissions import IsCommunityModerator
from helpers.update_reactions import add_popularity
from helpers.notify import notify_author
from hide.models import Hide
from helpers.publication import check_publication_update_date_limit
from publication.serializers import *


class PublicationListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PublicationSerializer
    authentication_classes = []
    permission_classes = []
    filterset_fields = [
        "created_by",
        "is_published",
        "created_at",
        "type",
        "community",
        "is_pinned",
    ]

    def get_queryset(self):
        filterset, sort_string = helper.get_viewset_filterset(
            self.request, self.filterset_fields, "published_at"
        )
        user = helper.get_user_from_auth_header(self.request)

        queryset = Publication.objects.filter(**filterset).order_by(sort_string)
        hidden_publications = []
        if user:
            hides = Hide.objects.filter(publication__isnull=False)
            [hidden_publications.append(hide.publication.id) for hide in hides]
        return queryset.exclude(id__in=hidden_publications)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["depth"] = int(self.request.query_params.get("depth", 0))
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
    permission_classes = [IsOwner | IsCommunityModerator]

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
    permission_classes = [IsOwner | IsCommunityModerator]

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
        # recorded only at the first time of publishing
        # to notice first time of publishing
        if not publication.published_at:
            if publication.community:
                add_popularity(publication)
                published_by = publication.created_by
                description = (
                    f"{published_by.profile.display_name or published_by.created_by.username}"
                    f" published a new publication in the community "
                    f'"{publication.community.name}".'
                )
                notify_author(
                    target=publication.community,
                    instance=publication,
                    key="publication",
                    description=description,
                )
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
        publication.save()
        return Response(status=status.HTTP_201_CREATED)


class PublicationPinView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner | IsCommunityModerator]

    def patch(self, request, pk=None):
        publication = get_object_or_404(Publication, pk=pk)
        self.check_object_permissions(request, publication)
        if not publication.is_published:
            return Response(
                {"detail": ["Publication not published yet."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if publication.is_pinned:
            return Response(status=status.HTTP_200_OK)
        publication.is_pinned = True
        publication.pinned_at = timezone.now()
        publication.pinned_by = request.user
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


class GetAPublication(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get(request, pk=None):
        publication = get_object_or_404(Publication, pk=pk)
        if publication.is_published:
            requestor = helper.get_user_from_auth_header(request)
            if requestor:
                _, created = RecentPublication.objects.get_or_create(
                    created_by=requestor, publication=publication
                )
                if created:
                    publication.views += 1
                    publication.save()
        serializer = PublicationSerializer(publication)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecentPublicationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def delete(request, pk):
        publication = get_object_or_404(Publication, pk=pk)
        try:
            recent_publication = RecentPublication.objects.get(
                created_by=request.user, publication=publication
            )
            recent_publication.delete()
            return Response(status=status.HTTP_200_OK)
        except RecentPublication.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
