from rest_framework import viewsets, serializers, mixins, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from account.permissions import IsSuperUser
from administration.models import Administration, PageView


class AdministrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administration
        exclude = ["id"]


class AdministrationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]
    serializer_class = AdministrationSerializer
    queryset = Administration.objects.all()

    def list(self, request, *args, **kwargs):
        administration = Administration.objects.first()
        if not administration:
            administration = Administration.objects.create()
        return Response(
            AdministrationSerializer(administration).data,
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        administration = Administration.objects.first()
        if not administration: administration = Administration.objects.create()

        serializer = AdministrationSerializer(
            administration,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        exclude = ["id"]


class PageViewViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]
    serializer_class = PageViewSerializer
    queryset = PageView.objects.all()

    def list(self, request, *args, **kwargs):
        page_view = PageView.objects.first()
        if not page_view:
            page_view = PageView.objects.create()
        return Response(
            PageViewSerializer(page_view).data,
            status=status.HTTP_200_OK
        )

    @staticmethod
    def create(request, *args, **kwargs):
        # instance check
        page_view = PageView.objects.first()
        if not page_view: page_view = PageView.objects.create()

        # validate query param count
        if len(request.query_params) > 1:
            return Response({
                "detail": "Only single query parameter is allowed."
            }, status=status.HTTP_400_BAD_REQUEST)

        # fetch query param
        homepage = request.query_params.get('homepage')
        publications = request.query_params.get('publications')
        community = request.query_params.get('community')
        profile = request.query_params.get('profile')
        settings = request.query_params.get('settings')
        administration = request.query_params.get('administration')

        # if query param is available and true when parsed to integer then add count
        if homepage and bool(int(homepage)): page_view.homepage += 1
        elif publications and bool(int(publications)): page_view.publications += 1
        elif community and bool(int(community)): page_view.community += 1
        elif profile and bool(int(profile)): page_view.profile += 1
        elif settings and bool(int(settings)): page_view.settings += 1
        elif administration and bool(int(administration)): page_view.administration += 1
        else: pass

        page_view.save()

        return Response(
            PageViewSerializer(page_view).data,
            status=status.HTTP_200_OK
        )
