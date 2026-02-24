from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt_handler import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/auth/login")

# def get_current_user_id(token: str = Depends(oauth2_schema)):
#     try:
#         # print(oauth2_schema)
        
#         payload = decode_token(token)
#         print("Token:", token)
#         print("payload: ", payload)
#     except ValueError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="gaya Invalid or expired token"
#         )
    
#     if payload.get("type") != "access":
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail= "Invalid token type"
#         )
        
#     user_id = payload.get("sub")
#     if not user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token payload"
#         )
#     return int(user_id)


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        print("DEBUG: raw token =", token)

        payload = decode_token(token)
        print("DEBUG: decoded payload =", payload)

    except Exception as e:
        print("DEBUG: exception while decoding token =", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if payload.get("type") != "access":
        print("DEBUG: token type =", payload.get("type"))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    user_id = payload.get("sub")
    print("DEBUG: user_id =", user_id)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    return int(user_id)