import os
from typing import List

# H.1: fail-fast on truly required runtime config
REQUIRED_ENV_VARS: List[str] = [
    # core runtime
    "ENV",
    "DATABASE_URL",

    # auth
    "SECRET_KEY",
    "JWT_ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "REFRESH_TOKEN_EXPIRE_DAYS",

    # storage (your app.services.storage requires these)
    "MINIO_ENDPOINT",
    "MINIO_ACCESS_KEY",
    "MINIO_SECRET_KEY",
    "MINIO_SECURE",
    "MINIO_BUCKET",
]

def validate_required_env() -> None:
    missing = [k for k in REQUIRED_ENV_VARS if os.getenv(k) in (None, "")]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")

