from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from account.permissions import IsSuperUser
from ban.models import Ban
from ban.serializers import CreateBanSerializer


class BanAModelItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def post(self, request, *args, **kwargs):
        serializer = CreateBanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(banned_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, *args, **kwargs):
        ban = Ban.objects.get(pk=pk)
        ban.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
