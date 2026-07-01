from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    RegisterSerializer,
    VerifyOtpSerializer,
    LoginSerializer,
    UserSerializer,
    LogoutSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from .services import (
    register_user,
    verify_otp,
    login_user,
    logout_user,
    forgot_password,
    reset_password,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    register_user(serializer.validated_data)

    return Response(
        {"message": "Registration successful. Please verify your email OTP."},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def otp_verification(request):
    serializer = VerifyOtpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response_data = verify_otp(serializer.validated_data)

    return Response(
        response_data,
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response_data = login_user(serializer.validated_data)

    return Response(
        response_data,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def whoami(request):
    serializer = UserSerializer(request.user)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    serializer = LogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response_data = logout_user(serializer.validated_data)

    return Response(
        response_data,
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def password_forgot(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response_data = forgot_password(serializer.validated_data)

    return Response(
        response_data,
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset(request):
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response_data = reset_password(serializer.validated_data)

    return Response(
        response_data,
        status=status.HTTP_200_OK,
    )
