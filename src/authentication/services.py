import secrets
import string

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from django.db import transaction, IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from decouple import config

from .models import User

from .tasks import send_otp_email_task

LOGIN_ATTEMPT_LIMIT = config("LOGIN_ATTEMPT_LIMIT", cast=int)
LOGIN_ATTEMPT_TIMEOUT = config("LOGIN_ATTEMPT_TIMEOUT", cast=int)
OTP_TIMEOUT = config("OTP_TIMEOUT", cast=int)
FORGOT_TOKEN_TIMEOUT = config("FORGOT_TOKEN_TIMEOUT", cast=int)


def generate_otp(length=6):
    return "".join(secrets.choice(string.digits) for _ in range(length))


@transaction.atomic()
def register_user(validated_data):
    email = validated_data["email"]
    full_name = validated_data["full_name"]
    phone_number = validated_data["phone_number"]
    password = validated_data["password"]

    user = User.objects.select_for_update().only(
        "id",
        "email",
        "is_verified",
        "phone_number",
    ).filter(email=email).first()

    phone_taken = User.objects.filter(phone_number=phone_number).exclude(
        email=email
    ).exists()

    if phone_taken:
        raise ValidationError("Phone number already exists.")

    if user:
        if user.is_verified:
            raise ValidationError("Email already registered.")

        user.full_name = full_name
        user.phone_number = phone_number
        user.set_password(password)

        user.save(
            update_fields=[
                "full_name",
                "phone_number",
                "password",
            ]
        )

    else:
        try:
            user = User.objects.create_user(
                email=email,
                full_name=full_name,
                phone_number=phone_number,
                password=password,
            )

        except IntegrityError:
            raise ValidationError("Registration failed. Try again.")

    otp = generate_otp()

    cache.set(f"otp:{email}", otp, timeout=OTP_TIMEOUT)
    send_otp_email_task.delay(email, otp)

    return user


def verify_otp(validated_data):
    email = validated_data["email"]
    otp = validated_data["otp"]

    cached_otp = cache.get(f"otp:{email}")

    if cached_otp is None:
        raise ValidationError("OTP Expired or invalid.")
    
    if not secrets.compare_digest(cached_otp, otp):
        raise ValidationError("Invalid OTP.")
    
    user = User.objects.filter(email=email).first()

    if not user:
        raise ValidationError("User not found.")

    user.is_verified = True
    user.save(update_fields=["is_verified"])

    cache.delete(f"otp:{email}")

    return {
        "message": "Email verified successfully."
    }


def login_user(validated_data):
    email = validated_data["email"]
    password = validated_data["password"]

    attempts = cache.get(f"login_attempt:{email}", 0)

    if attempts >= LOGIN_ATTEMPT_LIMIT:
        raise ValidationError("Too many failed login attempts. Please try again after 5 minutes.")
    

    user = User.objects.filter(email=email).first()

    if not user or not User.check_password(password):
        attempts +=1
        cache.set(f"login_attempt:{email}", attempts, timeout=LOGIN_ATTEMPT_TIMEOUT)
        raise ValidationError("Invalid email or password.")

    if not user.is_verified:
        raise ValidationError("Please verify your email first.")

    if not user.is_active:
        raise ValidationError("Your account has been disabled.")

    cache.delete(f"login_attempt:{email}")
    refresh = RefreshToken.for_user(user)

    return {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "message": "Logged in successfully.",
    }


def logout_user(validated_data):
    refresh = validated_data["refresh"]

    try:
        token = RefreshToken(refresh)
        token.blacklist()

    except Exception:
        raise ValidationError("Invalid or expired refresh token.")
    
    return {"message": "Logged out successfully."}


def forgot_password(validated_data):
    email = validated_data["email"]

    user = User.objects.filter(email=email).first()

    if not user:
        raise ValidationError("User doesn't exist")
    
    if not user.is_verified:
        raise ValidationError("Please verify your email first.")
    
    token = secrets.token_urlsafe(32)

    cache.set(f"password_reset:{token}", email, timeout=FORGOT_TOKEN_TIMEOUT)

    reset_link = f"http://127.0.0.1:8000/api/v1/auth/reset-password/?token={token}"

    try:
        send_mail(
            subject="Reset your password",
            message=f"Click the link below to reset your password:\n\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

    except Exception:
        cache.delete(f"password_reset:{token}")
        raise ValidationError("Something went wrong. Failed to send password reset link.")

    return {
        "message": "Password reset link sent successfully."
    }


def reset_password(validated_data):
    token = validated_data["token"]
    new_password = validated_data["new_password"]

    email = cache.get(f"password_reset:{token}")

    if not email:
        raise ValidationError("Invalid or expired reset token.")
    
    user = User.objects.filter(email=email).first()

    if not user:
        raise ValidationError("User not found.")
    
    if user.check_password(new_password):
        raise ValidationError(
            "New password cannot be the same as your current password."
        )
    
    validate_password(new_password, user)
    
    try:
        user.set_password(new_password)
        user.save(update_fields=["password"])

    except Exception:
        raise ValidationError("Something went wrong. Failed to reset password.")
    
    cache.delete(f"password_reset:{token}")

    return {
        "message": "Password reset successfully."
    }




