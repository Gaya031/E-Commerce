import asyncio
import smtplib
import ssl
from email.message import EmailMessage

from app.core.config import settings
from app.core.logging import logger


def _email_enabled() -> bool:
    if not settings.EMAILS_ENABLED:
        return False
    if not settings.SMTP_HOST or not settings.SMTP_FROM_EMAIL:
        logger.warning("Email disabled: SMTP_HOST/SMTP_FROM_EMAIL missing")
        return False
    return True


def _send_sync(message: EmailMessage) -> None:
    context = ssl.create_default_context()
    if settings.SMTP_USE_SSL:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context, timeout=15) as server:
            if settings.SMTP_USERNAME:
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(message)
        return

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as server:
        if settings.SMTP_USE_TLS:
            server.starttls(context=context)
        if settings.SMTP_USERNAME:
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(message)


async def send_email(to: str, subject: str, body_text: str, body_html: str | None = None) -> bool:
    if not _email_enabled():
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
    message["To"] = to
    message.set_content(body_text)
    if body_html:
        message.add_alternative(body_html, subtype="html")

    try:
        await asyncio.to_thread(_send_sync, message)
        logger.info("Email sent to %s subject=%s", to, subject)
        return True
    except Exception as exc:
        logger.exception("Email send failed for %s: %s", to, str(exc))
        return False


def send_email_background(to: str, subject: str, body_text: str, body_html: str | None = None) -> None:
    async def _runner():
        await send_email(to=to, subject=subject, body_text=body_text, body_html=body_html)

    try:
        asyncio.create_task(_runner())
    except RuntimeError:
        logger.warning("No event loop available for background email: %s", subject)
