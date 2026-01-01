from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hashed(password: str) -> str:
    # bcrypt max allowed length = 72 bytes
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    print(plain_password)
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)
