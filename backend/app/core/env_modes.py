import os

ALLOWED_ENVS = {"development", "staging", "production"}


def get_env() -> str:
    return (os.getenv("ENV") or "development").strip().lower()


def validate_env_mode() -> str:
    env = get_env()
    if env not in ALLOWED_ENVS:
        raise RuntimeError(f"ENV must be one of {sorted(ALLOWED_ENVS)}")
    return env


def validate_production_requirements() -> None:
    env = validate_env_mode()
    if env != "production":
        return

    jwt_secret = os.getenv("JWT_SECRET") or ""
    refresh_secret = os.getenv("JWT_REFRESH_SECRET") or ""
    cors = os.getenv("CORS_ALLOWLIST") or ""

    if len(jwt_secret) < 32 or len(refresh_secret) < 32:
        raise RuntimeError("Production requires JWT secrets length >= 32")

    # In prod, forbid wildcard allowlist
    if "*" in cors:
        raise RuntimeError("Production CORS allowlist must not contain '*'")

