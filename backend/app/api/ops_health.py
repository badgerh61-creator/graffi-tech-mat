from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.ops_checks import compute_readiness

router = APIRouter(tags=["ops"])

@router.get("/health")
def health():
    """
    Liveness: must never touch DB.
    """
    return {"status": "ok", "service": "api"}


@router.get("/ready")
def ready(db: Session = Depends(get_db)):
    """
    Readiness: may touch DB (read-only).
    """
    result = compute_readiness(db=db)
    if not result.ready:
        # 503 indicates not ready for traffic
        return {"ready": False, "checks": result.checks, "status_code": 503}
    return {"ready": True, "checks": result.checks}
