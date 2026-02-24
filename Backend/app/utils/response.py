from typing import Any, Optional


def success_response(*, data: Optional[Any] = None, message: str = "Success",) -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(*, message: str, code: str = "ERROR",) -> dict:
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
