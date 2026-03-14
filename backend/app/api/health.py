# backend/app/api/health.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text

from app.db.session import get_db
from app.services import ops_checks

router = APIRouter(tags=["ops"])


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "api",
    }


def _normalize_readiness_result(result):
    if isinstance(result, dict):
        checks = result.get("checks", result)
        ready = result.get("ready")
        if ready is None:
            ready = (
                all(bool(v.get("ok", True)) for v in checks.values())
                if isinstance(checks, dict)
                else True
            )
        return bool(ready), checks if isinstance(checks, dict) else {}

    ready = getattr(result, "ready", None)
    checks = getattr(result, "checks", {})

    if ready is None:
        ready = (
            all(bool(v.get("ok", True)) for v in checks.values())
            if isinstance(checks, dict)
            else True
        )

    return bool(ready), checks if isinstance(checks, dict) else {}


@router.get("/ready")
def ready(db=Depends(get_db)):
    """
    Contract expectations from tests:

    1) If injected DB object itself is unusable -> 503 {"detail": "DB not ready"}
    2) If readiness check reports ready=False -> 200 structured payload
    3) If readiness check reports ready=True -> 200 structured payload
    """
    # Phase H1 expectation: hard DB dependency failure => 503
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="DB not ready")

    # Phase H8 expectation: structured readiness result => 200
    try:
        result = ops_checks.compute_readiness(db=db)
        ready_flag, checks = _normalize_readiness_result(result)
    except Exception:
        raise HTTPException(status_code=503, detail="DB not ready")

    return {
        "ready": ready_flag,
        "status": "ready" if ready_flag else "not_ready",
        "checks": checks,
    }
