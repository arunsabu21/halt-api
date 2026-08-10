import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY


def send_mail(*, to: str, subject: str, html: str):
    params: resend.Emails.SendParams = {
        "from": settings.DEFAULT_FROM_EMAIL,
        "to": [to],
        "subject": subject,
        "html": html,
    }

    return resend.Emails.send(params)
