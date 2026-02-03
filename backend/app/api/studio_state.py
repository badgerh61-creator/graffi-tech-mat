from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.snapshot import Snapshot
from app.services.studio_state_guard import get_blocked_execution_context

router = APIRouter(prefix="/studio", tags=["studio"])


@router.get("/state")
def get_studio_state(
    project_id: int | None = Query(None),
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    """
    Phase E.1 — Read-only studio state.
    No mutation. No side effects. Ever.
    """

    # Resolve project (read-only)
    if project_id is None:
        project_id = (
            db.query(Snapshot.project_id)
            .order_by(Snapshot.created_at.desc())
            .limit(1)
            .scalar()
        )

    snapshots = (
        db.query(Snapshot)
        .filter(Snapshot.project_id == project_id)
        .order_by(Snapshot.created_at.desc())
        .all()
    )

    # 🔒 Phase E.1 rule:
    # Prefer active DRAFT snapshot for studio context
    active = next(
        (s for s in snapshots if s.is_draft),
        snapshots[0] if snapshots else None,
    )

    # 🔒 Phase E.1 — ALWAYS mirror kernel block context (READ-ONLY)
    blocked = get_blocked_execution_context(
        db=db,
        user=user,
        snapshot=active,
    )

    block_reason = (
        {
            "code": blocked.get("code", "snapshot.locked"),
            "reason": blocked.get("reason"),
        }
        if blocked
        else None
    )

    return {
        "project_id": project_id,

        # Phase E.1 REQUIRED visibility (derived, not persisted)
        "station": "geometry",
        "mode": "edit",

        # Snapshot state
        "active_snapshot_id": active.id if active else None,
        "snapshot_status": active.status if active else None,

        # Ownership resolution (read-only helper)
        "draft_ownership": (
            active.resolve_ownership(user)
            if active
            else "not_applicable"
        ),

        # Kernel truth, mirrored
        "block_reason": block_reason,
    }

