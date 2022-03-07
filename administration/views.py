from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Profile
from account.permissions import IsSuperUser
from account.serializers.user import UserRetrieveSerializer
from administration.models import Administration, PageView
from administration.serializers import AdministrationSerializer, PageViewSerializer
from community.models import Community
from community.serializers.community import RetrieveSerializer


class AdministrationViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]
    serializer_class = AdministrationSerializer
    queryset = Administration.objects.all()

    def list(self, request, *args, **kwargs):
        instance = Administration.objects.first()
        if not instance:
            instance = Administration.objects.create()
        return Response(
            AdministrationSerializer(instance).data, status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        instance = Administration.objects.first()
        if not instance:
            instance = Administration.objects.create()

        serializer = AdministrationSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PageViewViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]
    serializer_class = PageViewSerializer
    queryset = PageView.objects.all()

    def list(self, request, *args, **kwargs):
        page_view = PageView.objects.first()
        if not page_view:
            page_view = PageView.objects.create()
        return Response(PageViewSerializer(page_view).data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request, *args, **kwargs):
        # instance check
        page_view = PageView.objects.first()
        if not page_view:
            page_view = PageView.objects.create()

        # validate query param count
        if len(request.query_params) > 1:
            return Response(
                {"detail": "Only single query parameter is allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # fetch query param
        homepage = request.query_params.get("homepage", None)
        publications = request.query_params.get("publications", None)
        community = request.query_params.get("community", None)
        profile = request.query_params.get("profile", None)
        settings = request.query_params.get("settings", None)
        administration = request.query_params.get("administration", None)

        # if query param is available and true when parsed to integer then add count
        if homepage and bool(int(homepage)):
            page_view.homepage += 1
        elif publications and bool(int(publications)):
            page_view.publications += 1
        elif community and bool(int(community)):
            page_view.community += 1
        elif profile and bool(int(profile)):
            page_view.profile += 1
        elif settings and bool(int(settings)):
            page_view.settings += 1
        elif administration and bool(int(administration)):
            page_view.administration += 1
        else:
            pass

        page_view.save()

        return Response(PageViewSerializer(page_view).data, status=status.HTTP_200_OK)


class TopView(APIView):
    @staticmethod
    def get(request):
        administration, created = Administration.objects.get_or_create(id=1)
        count = administration.top_count
        limit = administration.popularity_threshold
        communities = Community.objects.filter(
            type__in=["public", "restricted"],
            popularity__gte=limit,
        ).order_by("-popularity")[:count]

        profiles = Profile.objects.filter(popularity__gte=limit).order_by(
            "-popularity"
        )[:count]
        users = []
        [users.append(profile.user) for profile in profiles]

        profiles = Profile.objects.filter(discussions__gte=limit,).order_by(
            "-discussions"
        )[:count]
        commentators = []
        [commentators.append(profile.user) for profile in profiles]

        context = {"user": request.user}

        return Response(
            {
                "communities": RetrieveSerializer(
                    communities, many=True, context=context
                ).data,
                "users": UserRetrieveSerializer(users, many=True, context=context).data,
                "commentators": UserRetrieveSerializer(
                    commentators, many=True, context=context
                ).data,
            },
            status=status.HTTP_200_OK,
        )
