from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from account.permissions import IsSuperUser
from ban.models import Ban
from ban.serializers import BanSerializer


class BanAModelItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            ban = Ban.objects.get(pk=pk)
            serializer = BanSerializer(ban)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            bans = Ban.objects.all()
            serializer = BanSerializer(bans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = BanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(banned_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, *args, **kwargs):
        ban = Ban.objects.get(pk=pk)
        ban.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
