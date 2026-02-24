import time
from fastapi import Request, HTTPException, status
from redis.asyncio import Redis
from app.db.redis import get_redis

class RateLimiter:
    def __init__(self, limit: int, window_seconds: int, key_prefix: str):
        self.limit = limit
        self.window = window_seconds
        self.key_prefix = key_prefix
        
    async def __call__(self, request: Request):
        redis: Redis = await get_redis()
        
        ip = request.client.host if request.client else "unknown"
        path = request.url.path
        
        key = f"rate:{self.key_prefix}:{ip}:{path}"
        now = int(time.time())
        
        current = await redis.incr(key)
        
        if current == 1:
            await redis.expire(key, self.window)
            
        if current > self.limit:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="too many requests. Please try again later.")
        