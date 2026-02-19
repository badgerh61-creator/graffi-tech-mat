from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


@dataclass(frozen=True)
class SecuritySettings:
    # IMPORTANT: plain defaults only (env is read in from_env)
    enable_security_headers: bool = True
    enable_strict_cors: bool = False
    enable_login_rate_limit: bool = False

    login_rate_limit_window_seconds: int = 60
    login_rate_limit_max_requests: int = 30

    cors_allow_origins_csv: str = ""

    def cors_allow_origins(self) -> list[str]:
        if not self.cors_allow_origins_csv.strip():
            return []
        return [o.strip() for o in self.cors_allow_origins_csv.split(",") if o.strip()]

    @classmethod
    def from_env(cls) -> "SecuritySettings":
        return cls(
            enable_security_headers=_env_bool("GTM_ENABLE_SECURITY_HEADERS", True),
            enable_strict_cors=_env_bool("GTM_ENABLE_STRICT_CORS", False),
            enable_login_rate_limit=_env_bool("GTM_ENABLE_LOGIN_RATE_LIMIT", False),
            login_rate_limit_window_seconds=_env_int("GTM_LOGIN_RL_WINDOW_SECONDS", 60),
            login_rate_limit_max_requests=_env_int("GTM_LOGIN_RL_MAX_REQUESTS", 30),
            cors_allow_origins_csv=os.getenv("GTM_CORS_ALLOW_ORIGINS", "") or "",
        )

