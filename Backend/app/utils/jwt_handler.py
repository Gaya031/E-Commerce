from datetime import datetime, timedelta, timezone
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from app.core.config import settings
from typing import Dict, Any

def _create_token(*, user_id: int, expires_delta: timedelta, token_type: str) -> str:
    now = datetime.now(tz = timezone.utc)
    payload = {
        "sub": str(user_id),
        "type": token_type,
        "iat": now,
        "nbf": now,
        "exp": now + expires_delta,
        "iss": settings.JWT_ISSUER
    }
    
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_access_token(user_id: int) -> str:
    return _create_token(
        user_id=user_id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access"
    )

def create_refresh_token(user_id: int) -> str:
    return _create_token(
        user_id=user_id,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh"
    )
    
def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], issuer=settings.JWT_ISSUER)
        return payload
    except ExpiredSignatureError:
        raise ValueError('Token has Expired')
    except InvalidTokenError as e:
        raise ValueError(f"Invalid token: {str(e)}")
    