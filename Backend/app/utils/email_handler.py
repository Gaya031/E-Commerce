async def send_email(to: str, subject: str, body: str):
    # Plug SendGrid / SES later
    # Keeping async signature for future
    print(f"[EMAIL] To:{to} | {subject}")
