from django.contrib.auth import authenticate, get_user_model, logout
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from account.permissions import IsSuperUser
from account.serializers.auth import LoginSerializer
from account.serializers.user import UserInfoSerializer
from administration.serializers import AdministrationSerializer, Administration


class AdminInspect(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    @staticmethod
    def get(request, username):
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserInfoSerializer(user, context={"request": request})
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user": serializer.data},
            status=status.HTTP_202_ACCEPTED,
        )


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        """
        Login a user instance
        Provides a brand new token for a member user
        """
        user_serializer = LoginSerializer(data=request.data)
        if user_serializer.is_valid():
            username = user_serializer.data["username"]
            password = user_serializer.data["password"]
            try:
                get_user_model().objects.get(username=username)
            except get_user_model().DoesNotExist:
                return Response(
                    {"detail": "User '" + username + "' Not Found!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            user = authenticate(username=username, password=password)
            if user:
                user.last_login = timezone.now()
                if not user.is_active:
                    user.is_active = True
                user.save()
                user_serializer = UserInfoSerializer(user, context={"request": request})
                administration_serializer = AdministrationSerializer(Administration.objects.get(pk=1))
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "token": token.key,
                        "user": user_serializer.data,
                        "administration": administration_serializer.data,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            return Response(
                {"detail": "Login failed! Provide valid authentication credentials."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        """
        Logs out a user instance
        Removes member user token from database
        """
        user = request.user
        if not user.is_authenticated:
            return Response(
                {"detail": "User not logged in."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        logout(request)
        token = Token.objects.get(user=user)
        token.delete()
        return Response(
            {"detail": "User '{}' logged out successfully.".format(user.username)},
            status=status.HTTP_204_NO_CONTENT,
        )
