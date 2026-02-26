from app.core.config import settings


def _app_url(path: str) -> str:
    base = settings.FRONTEND_URL.rstrip("/")
    return f"{base}/{path.lstrip('/')}"


def welcome_email(name: str) -> tuple[str, str]:
    subject = "Welcome to RushCart"
    text = (
        f"Hi {name},\n\n"
        "Welcome to RushCart. Your account is ready.\n"
        f"Start shopping: {_app_url('')}\n\n"
        "Thanks,\nRushCart Team"
    )
    return subject, text


def password_reset_email(name: str, token: str) -> tuple[str, str]:
    reset_link = _app_url(f"reset-confirmation?token={token}")
    subject = "Reset your RushCart password"
    text = (
        f"Hi {name},\n\n"
        "We received a request to reset your password.\n"
        f"Reset link: {reset_link}\n\n"
        "If you did not request this, ignore this email."
    )
    return subject, text


def order_created_email(name: str, order_id: int, amount: int) -> tuple[str, str]:
    subject = f"Order #{order_id} placed successfully"
    text = (
        f"Hi {name},\n\n"
        f"Your order #{order_id} has been placed.\n"
        f"Total amount: INR {amount}\n"
        f"Track order: {_app_url(f'buyer/order/{order_id}/tracking')}\n\n"
        "Thank you for shopping with RushCart."
    )
    return subject, text


def order_status_email(name: str, order_id: int, status: str) -> tuple[str, str]:
    subject = f"Order #{order_id} status updated"
    text = (
        f"Hi {name},\n\n"
        f"Your order #{order_id} is now '{status}'.\n"
        f"Track order: {_app_url(f'buyer/order/{order_id}/tracking')}"
    )
    return subject, text


def seller_approval_email(name: str, approved: bool) -> tuple[str, str]:
    subject = "Seller verification update"
    state = "approved" if approved else "rejected"
    text = (
        f"Hi {name},\n\n"
        f"Your seller profile has been {state}.\n"
        f"Dashboard: {_app_url('seller')}"
    )
    return subject, text


def refund_email(name: str, order_id: int) -> tuple[str, str]:
    subject = f"Refund processed for order #{order_id}"
    text = (
        f"Hi {name},\n\n"
        f"Refund for order #{order_id} has been processed.\n"
        f"Check wallet/orders: {_app_url('buyer/orders')}"
    )
    return subject, text
