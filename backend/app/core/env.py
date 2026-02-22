import os
from typing import List


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes", "on")


def _int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default


# ===== REQUIRED (always) =====
BASE_REQUIRED_ENV_VARS: List[str] = [
    "ENV",
    "DATABASE_URL",
    "SECRET_KEY",
]

# ===== AUTH DEFAULTS (safe for dev) =====
DEFAULTS = {
    "JWT_ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
    "REFRESH_TOKEN_EXPIRE_DAYS": "7",
    "MINIO_SECURE": "false",
}


def apply_defaults() -> None:
    """
    Apply safe defaults for development/ops mode.
    Does not override explicitly set values.
    """
    for key, value in DEFAULTS.items():
        if os.getenv(key) in (None, ""):
            os.environ[key] = value


def validate_required_env() -> None:
    """
    Fail-fast only for truly required core values.
    Storage and JWT values may have safe defaults in dev.
    """
    apply_defaults()

    missing = [k for k in BASE_REQUIRED_ENV_VARS if os.getenv(k) in (None, "")]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
