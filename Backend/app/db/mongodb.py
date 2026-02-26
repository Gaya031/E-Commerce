"""
Optional MongoDB hooks for future modules.
The current backend does not require MongoDB at runtime.
"""

from typing import Any

mongo_client: Any = None


async def init_mongodb() -> None:
    return None


async def get_mongodb() -> Any:
    return mongo_client


async def close_mongodb() -> None:
    return None
