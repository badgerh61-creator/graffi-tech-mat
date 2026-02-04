# backend/app/api/studio_tools.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.snapshot import Snapshot
from app.services.tool_availability import get_tool_availability

router = APIRouter(prefix="/studio", tags=["studio"])


@router.get("/tools")
def read_tool_availability(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Phase E.2 — Tool Availability

    - No required identifiers
    - No authority leaks
    - Context resolved internally
    """

    # 🔒 Same rule as studio_state
    snapshot = (
        db.query(Snapshot)
        .order_by(Snapshot.created_at.desc())
        .first()
    )

    return get_tool_availability(
        user=user,
        snapshot=snapshot,
        station=user.current_station,
    )

