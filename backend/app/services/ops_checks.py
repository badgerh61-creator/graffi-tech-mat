from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import text


@dataclass(frozen=True)
class ReadinessResult:
    ready: bool
    checks: Dict[str, Any]


def check_db_readiness(db: Session) -> tuple[bool, str]:
    """
    Read-only DB readiness check.
    Must be fast, deterministic, and safe for sqlite/postgres.
    """
    try:
        db.execute(text("SELECT 1"))
        return True, "ok"
    except Exception as e:  # pragma: no cover (we test via monkeypatch)
        return False, f"db_error:{type(e).__name__}"


def compute_readiness(*, db: Session) -> ReadinessResult:
    db_ok, db_msg = check_db_readiness(db)
    ready = bool(db_ok)

    return ReadinessResult(
        ready=ready,
        checks={
            "db": {
                "ok": db_ok,
                "detail": db_msg,
            }
        },
    )
