import asyncio
import time
from copy import deepcopy


_CACHE: dict[str, tuple[float, object]] = {}
_LOCK = asyncio.Lock()


async def cache_get(key: str):
    async with _LOCK:
        row = _CACHE.get(key)
        if not row:
            return None
        expires_at, value = row
        if expires_at < time.time():
            _CACHE.pop(key, None)
            return None
        return deepcopy(value)


async def cache_set(key: str, value, ttl_seconds: int):
    async with _LOCK:
        _CACHE[key] = (time.time() + ttl_seconds, deepcopy(value))


async def cache_delete_prefix(prefix: str):
    async with _LOCK:
        keys = [k for k in _CACHE if k.startswith(prefix)]
        for key in keys:
            _CACHE.pop(key, None)
