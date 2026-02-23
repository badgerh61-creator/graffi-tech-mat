# backend/app/api/health.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(tags=["ops"])


@router.get("/health")
def health():
    return {"status": "alive"}


@router.get("/ready")
def ready(db: Session = Depends(get_db)):
    # Must be safe + non-mutating
    try:
        db.execute("SELECT 1")
    except Exception:
        raise HTTPException(status_code=503, detail="DB not ready")
    return {"status": "ready"}
