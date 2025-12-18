from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# -------------------------------------------------------------------
# Password hashing configuration
# -------------------------------------------------------------------
# bcrypt has a hard 72-byte limit — we enforce safe truncation
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

BCRYPT_MAX_BYTES = 72
ALGORITHM = "HS256"


# -------------------------------------------------------------------
# Internal helpers
# -------------------------------------------------------------------
def _normalize_password(password: str) -> str:
    """
    bcrypt only supports the first 72 bytes.
    We *intentionally* truncate to prevent runtime crashes.
    """
    if password is None:
        return ""
    return password.encode("utf-8")[:BCRYPT_MAX_BYTES].decode("utf-8", errors="ignore")


# -------------------------------------------------------------------
# Password hashing
# -------------------------------------------------------------------
def get_password_hash(password: str) -> str:
    normalized = _normalize_password(password)
    return pwd_context.hash(normalized)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    normalized = _normalize_password(plain_password)
    return pwd_context.verify(normalized, hashed_password)


# -------------------------------------------------------------------
# JWT handling
# -------------------------------------------------------------------
def create_jwt_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.utcnow(),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )

