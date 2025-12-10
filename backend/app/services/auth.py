from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from ..core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    expire = datetime.utcnow() + timedelta(minutes=(expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {'sub': subject, 'exp': expire.isoformat()}
    encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256')
    return encoded
