from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsOwner
from auth_code.models import AuthorizationCode, ResetPasswordCode
from auth_code.serializers import (ResetNewPasswordSerializer,
                                   ResetPasswordEmailSerializer)
from backend import settings
from community.models import Community
from community.permissions import IsCommunityModerator


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


class RequestCommunityAuthorization(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityModerator]

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        self.check_object_permissions(request, community)
        if not community.email:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "Community does not have email set."},
            )
        if community.is_authorized:
            return Response(
                status=status.HTTP_204_NO_CONTENT,
                data={"detail": "Community is already authorized."},
            )
        codes = AuthorizationCode.objects.filter(
            community=community, created_by=request.user
        )
        [code.delete() for code in codes]  # delete every pre-requested codes
        code = AuthorizationCode.objects.create(
            community=community, created_by=request.user
        )
        mail_subject = "Authorize Community"
        message = render_to_string(
            "authorize_community.html",
            {
                "request": request,
                "user": request.user,
                "domain": get_current_site(request).domain,
                "code": code.code,
            },
        )
        send_mail(
            mail_subject,
            message="AuthorizeCommunity",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[community.email],
            html_message=message,
        )
        return Response(status=status.HTTP_200_OK)


class RequestUserAuthorization(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def post(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        self.check_object_permissions(request, user)
        if not user.email:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "User does not have email set."},
            )
        if user.profile.is_authorized:
            return Response(
                status=status.HTTP_204_NO_CONTENT,
                data={"detail": "User is already authorized."},
            )
        codes = AuthorizationCode.objects.filter(user=user, created_by=request.user)
        # delete every pre-requested codes
        [code.delete() for code in codes]
        code = AuthorizationCode.objects.create(user=user, created_by=request.user)
        mail_subject = "Authorize User"
        message = render_to_string(
            "authorize_user.html",
            {
                "request": request,
                "user": request.user,
                "domain": get_current_site(request).domain,
                "code": code.code,
            },
        )
        send_mail(
            mail_subject,
            message="AuthorizeUser",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=message,
        )
        return Response(status=status.HTTP_200_OK)


class ConfirmCommunityAuthorization(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCommunityModerator]

    def post(self, request, code):
        code = get_object_or_404(AuthorizationCode, code=code)
        self.check_object_permissions(request, code)
        community_to_authorize = code.community
        community_to_authorize.is_authorized = True
        community_to_authorize.authorized_at = timezone.now()
        community_to_authorize.save()
        code.delete()
        return Response(status=status.HTTP_200_OK)


class ConfirmUserAuthorization(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def post(self, request, code):
        code = get_object_or_404(AuthorizationCode, code=code)
        self.check_object_permissions(request, code)
        user_to_authorize = code.user.profile
        user_to_authorize.is_authorized = True
        user_to_authorize.authorized_at = timezone.now()
        user_to_authorize.save()
        code.delete()
        return Response(status=status.HTTP_200_OK)
