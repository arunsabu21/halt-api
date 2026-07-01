from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    register,
    otp_verification,
    login,
    whoami,
    logout,
    password_forgot,
    password_reset,
)

urlpatterns = [
    path("register/", register, name="register"),
    path("verify-otp/", otp_verification, name="verify-otp"),
    path("login/", login, name="login"),
    path("whoami/", whoami, name="whoami"),
    path("logout/", logout, name="logout"),
    path("forgot-password/", password_forgot, name="password-forgot"),
    path("reset-password/", password_reset, name="reset-password"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
