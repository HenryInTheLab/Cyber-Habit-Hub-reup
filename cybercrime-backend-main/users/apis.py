from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.exceptions import InvalidUserException, InvalidUserRecoveryException
from users.selectors import user_get_by_username
from users.serializers import (UserSerializer, UserSignedInSerializer,
                               UserSignInSerializer)
from users.services import user_create, user_update
from users.utils import (generate_recovery_phrase, initialize_account,
                         verify_code)


class UserDetailApi(APIView):
    permission_classes = [IsAuthenticated]

    class UserDetailResponseSerializer(serializers.Serializer):
        user = UserSerializer()

    @extend_schema(
        responses=UserDetailResponseSerializer,
        description="Get details of the currently authenticated user."
    )
    def get(self, request):
        user = request.user
        return Response(self.UserDetailResponseSerializer({
            "user": UserSerializer(user).data
        }).data)

class UserSignUpApi(APIView):
    class UserSignUpSerializer(serializers.Serializer):
        totp_secret = serializers.CharField()
        username = serializers.CharField()
        otp_uri = serializers.CharField()
        recovery_phrase = serializers.CharField()

    @extend_schema(
        responses=UserSignUpSerializer,
        description="Start sign-up: Generate a unique username, TOTP secret, and OTP URI for TOTP compatible applications."
    )
    def post(self, request):
        totp_secret, username, otp_uri = initialize_account()
        data = { "totp_secret": totp_secret, "username": username, "otp_uri": otp_uri, "recovery_phrase": generate_recovery_phrase() }
        return Response(self.UserSignUpSerializer(data).data)
    
class UserVerifyApi(APIView):
    class UserVerifySerializer(serializers.Serializer):
        totp_secret = serializers.CharField()
        username = serializers.CharField()
        code = serializers.CharField()
        recovery_phrase = serializers.CharField()

    @extend_schema(
        request=UserVerifySerializer,
        responses=UserSignedInSerializer,
        description="Verify the TOTP code for the given username. Returns user info and JWT tokens if successful."
    )
    def post(self, request):
        serializer = self.UserVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        totp_secret = serializer.validated_data["totp_secret"]
        username = serializer.validated_data["username"]
        code = serializer.validated_data["code"]
        recovery_phrase = serializer.validated_data["recovery_phrase"]
        
        if not verify_code(totp_secret, code): raise InvalidUserException()
        user = user_create(username=username, totp_secret=totp_secret, recovery_phrase=recovery_phrase)

        refresh_token = RefreshToken.for_user(user)
        return Response(UserSignedInSerializer({
            "user": UserSerializer(user).data,
            "refresh_token": str(refresh_token),
            "access_token": str(refresh_token.access_token),
        }).data)

class UserSignInApi(APIView):
    @extend_schema(
        request=UserSignInSerializer,
        responses=UserSignedInSerializer,
        description="Sign in: Verify the TOTP code for the given username. Returns user info and JWT tokens if successful."
    )
    def post(self, request):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = user_get_by_username(serializer.validated_data["username"])
        if not user or not verify_code(user.totp_secret, serializer.validated_data["code"]): raise InvalidUserException()
        
        refresh_token = RefreshToken.for_user(user)
        return Response(UserSignedInSerializer({
            "user": UserSerializer(user).data,
            "refresh_token": str(refresh_token),
            "access_token": str(refresh_token.access_token),
        }).data)

class UserRecoveryApi(APIView):
    class UserRecoveryInputSerializer(serializers.Serializer):
        username = serializers.CharField()
        recovery_phrase = serializers.CharField()

    class UserRecoveryOutputSerializer(serializers.Serializer):
        totp_secret = serializers.CharField()
        otp_uri = serializers.CharField()

    @extend_schema(
        request=UserRecoveryInputSerializer,
        responses=UserRecoveryOutputSerializer,
        description="Recover account using username and recovery phrase. Returns a new TOTP secret and OTP URI for TOTP compatible applications."
    )
    def post(self, request):
        serializer = self.UserRecoveryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_get_by_username(serializer.validated_data["username"])
        if not user or not check_password(serializer.validated_data["recovery_phrase"], getattr(user, "recovery_phrase_hash", "")):
            raise InvalidUserRecoveryException()

        totp_secret, _, otp_uri = initialize_account(user.username)
        user = user_update(user=user, data={"totp_secret": totp_secret})

        return Response(self.UserRecoveryOutputSerializer({
            "totp_secret": totp_secret,
            "otp_uri": otp_uri,
        }).data)
