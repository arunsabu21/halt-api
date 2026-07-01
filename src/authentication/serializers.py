from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^[6-9]\d{9}$",
                message="Enter a valid 10-digit Indian mobile number.",
            )
        ],
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True,
    )

    def validate_password(self, value):
        validate_password(value)
        return value


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(
        min_length=6,
        max_length=6,
        validators=[
            RegexValidator(
                regex=r"^\d{6}$",
                message="OTP must contain exactly 6 digits",
            )
        ],
    )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "phone_number", "created_at"]
        read_only_fields = ["id", "created_at"]


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                "Passwords do not match"
            )
        
        return attrs
