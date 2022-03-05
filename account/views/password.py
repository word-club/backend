from django.contrib.auth import authenticate, get_user_model, update_session_auth_hash

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers.password import UpdatePasswordSerializer


class UpdatePassword(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        """
        Update password for authenticated user
        """
        serializer = UpdatePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            username = request.user.username
            password = serializer.validated_data["password"]
            new_password = serializer.validated_data["new_password"]
            try:
                get_user_model().objects.get(username=username)
                user = authenticate(username=username, password=password)
                if user:
                    user.set_password(new_password)
                    user.save()
                    # Remove existing token after changing password
                    token = Token.objects.get(user=user)
                    token.delete()
                    update_session_auth_hash(request, request.user)
                    return Response(
                        {"message": "Update password success."},
                        status=status.HTTP_204_NO_CONTENT,
                    )
                else:
                    return Response(
                        {"detail": "Wrong existing password."},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            except get_user_model().DoesNotExist:
                return Response(
                    {"detail": "User does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
