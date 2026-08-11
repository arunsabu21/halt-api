from celery import shared_task
from core.email.resend import send_mail


@shared_task
def send_otp_email_task(email, otp):
    html = f"""
    <div style="font-family: Helvetica, sans-serif; max-width: 480px; margin: 0 auto;">
        <h2 style="color: #1a1f1c;">Your OTP Code</h2>
        <p style="font-size: 24px; font-weight: 700; letter-spacing: 4px; color: #2d5f4c;">{otp}</p>
        <p style="color: #6b7570; font-size: 13px;">This code expires shortly. If you didn't request this, ignore this email.</p>
    </div>
    """
    send_mail(to=email, subject="Your OTP Code", html=html)


@shared_task
def send_password_reset_email_task(email, reset_link):
    html = f"""
    <div style="font-family: Helvetica, sans-serif; max-width: 480px; margin: 0 auto;">
        <h2 style="color: #1a1f1c;">Reset Your Password</h2>
        <p style="color: #6b7570; font-size: 13px;">Click below to reset your password. This link expires shortly.</p>
        <a href="{reset_link}" style="display: inline-block; background: #2d5f4c; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; margin-top: 12px;">Reset Password</a>
    </div>
    """
    send_mail(to=email, subject="Reset your password", html=html)
