import re


def validate_phone(phone: str) -> bool:
    return bool(re.fullmatch(r"[6-9]\d{9}", phone))


def validate_pincode(pincode: str) -> bool:
    return bool(re.fullmatch(r"\d{6}", pincode))
