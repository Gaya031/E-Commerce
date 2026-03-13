from app.core.config import settings
from app.utils.email_templates import order_status_email, password_reset_email, welcome_email


def test_subscription_enforcement_default_is_enabled():
    assert settings.ENFORCE_SELLER_SUBSCRIPTION is True


def test_welcome_email_contains_frontend_link():
    subject, body = welcome_email("Demo")
    assert "Welcome to RushCart" in subject
    assert settings.FRONTEND_URL.rstrip("/") in body


def test_password_reset_email_contains_tokenized_link():
    _subject, body = password_reset_email("Demo", "abc123")
    assert "abc123" in body
    assert "/reset-confirmation?token=abc123" in body


def test_order_status_email_contains_tracking_link():
    _subject, body = order_status_email("Demo", 41, "shipped")
    assert "/buyer/order/41/tracking" in body
