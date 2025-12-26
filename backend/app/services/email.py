from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging

from app.core.config import settings

log = logging.getLogger(__name__)


def send_invite_email(
    *,
    to_email: str,
    model_name: str,
    role: str,
    token: str,
):
    """
    Send model collaboration invite email.

    SAFE:
    - Never raises outward
    - Failure does NOT block invite creation
    """
    if not settings.SENDGRID_API_KEY:
        log.warning("SendGrid API key missing — email skipped")
        return

    invite_url = (
        f"{settings.FRONTEND_BASE_URL}/invite/{token}"
    )

    subject = "You’ve been invited to collaborate on a model"

    content = f"""
You’ve been invited to collaborate on the model "{model_name}".

Role: {role}

Accept invite:
{invite_url}

This link expires in 7 days.
"""

    message = Mail(
        from_email=settings.EMAIL_FROM,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
        log.info("Invite email sent to %s", to_email)
    except Exception as exc:
        log.exception("Failed to send invite email: %s", exc)

