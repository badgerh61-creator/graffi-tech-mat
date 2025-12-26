# backend/app/api/exports.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import require_viewer

router = APIRouter(
    prefix="/exports",
    tags=["exports"],
)


@router.get("/health")
def exports_health(
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    """
    Phase A stub endpoint.

    Confirms:
    - router wiring
    - auth
    - db access

    Real export logic comes later.
    """
    return {
        "status": "ok",
        "exports": "ready",
    }

