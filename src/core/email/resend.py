import base64
import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY


def send_mail(*, to: str, subject: str, html: str, attachments: list | None = None):
    params: resend.Emails.SendParams = {
        "from": settings.DEFAULT_FROM_EMAIL,
        "to": [to],
        "subject": subject,
        "html": html,
    }

    if attachments:
        params["attachments"] = [
            {
                "filename": name,
                "content": list(base64.b64decode(base64.b64encode(content))),
            }
            for name, content in attachments
        ]

    return resend.Emails.send(params)
