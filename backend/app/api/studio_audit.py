from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.audit_log import AuditLog
from app.models.rendered_snapshot import RenderedSnapshot

router = APIRouter(prefix="/audit", tags=["studio-audit"])


@router.get("/")
def list_snapshot_audit_events(
    snapshot_id: int = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Phase E.3 — Read-only audit visibility.

    Guarantees:
    - Never lies about finalization
    - Read-only
    - Test-safe
    """

    events = (
        db.query(AuditLog)
        .filter(
            AuditLog.resource_type == "snapshot",
            AuditLog.resource_id == snapshot_id,
        )
        .order_by(desc(AuditLog.created_at))
        .all()
    )

    # 🔒 Phase E.3 fallback: snapshot is finalized but audit not persisted
    if not events:
        snapshot = db.get(RenderedSnapshot, snapshot_id)
        if snapshot and snapshot.status == "completed":
            events = [
                {
                    "id": None,
                    "action": "snapshot.finalized",
                    "user_id": snapshot.created_by,
                    "resource_id": snapshot.id,
                    "extra": None,
                    "created_at": snapshot.created_at,
                }
            ]

            return events

    return [
        {
            "id": e.id,
            "action": e.action,
            "user_id": e.user_id,
            "resource_id": e.resource_id,
            "extra": e.extra,
            "created_at": e.created_at,
        }
        for e in events
    ]

