from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import ResetPasswordCode
from account.serializers.password import (
    ResetNewPasswordSerializer,
    ResetPasswordEmailSerializer,
    UpdatePasswordSerializer,
)


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


class ResetPasswordRequestCode(APIView):
    permission_classes = ()
    authentication_classes = ()

    @staticmethod
    def post(request):
        """
        Reset user password -> Sends PIN to provided email address
        """
        serializer = ResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = get_user_model().objects.get(email=email)

                current_site = get_current_site(request)
                code_object, created = ResetPasswordCode.objects.get_or_create(
                    user=user
                )
                if not created:
                    code_object.delete()
                    code_object = ResetPasswordCode.objects.create(user=user)
                code = code_object.code
                mail_subject = "Reset user password"
                message = render_to_string(
                    "reset_email.html",
                    {
                        "user": user.username,
                        "domain": current_site.domain,
                        "code": code,
                    },
                )
                send_mail(
                    mail_subject,
                    message="ResetPassword",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    html_message=message,
                )
                return Response(
                    {"detail": "Reset-password link sent to provided mail address."},
                    status=status.HTTP_202_ACCEPTED,
                )
            except get_user_model().DoesNotExist:
                return Response(
                    {"detail": "User not found."}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmResetPassword(APIView):
    """
    Confirm Reset Password
    """

    permission_classes = ()
    authentication_classes = ()

    @staticmethod
    def post(request, code):
        serializer = ResetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data["new_password"]
            try:
                reset_password_code = ResetPasswordCode.objects.get(code=code)
                user = reset_password_code.user
                user.set_password(password)
                user.save()
                reset_password_code.delete()
                return Response(
                    {"message": "Reset password success."}, status=status.HTTP_200_OK
                )
            except ResetPasswordCode.DoesNotExist:
                return Response(
                    {"detail": "Code not found."}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
