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
    user=Depends(get_current_user),
):
    """
    Phase E.1–E.3 — Read-only studio state.
    No mutation. No side effects. Ever.
    """

    # Resolve project (read-only fallback)
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

    # 🔒 Prefer active DRAFT snapshot
    active = next(
        (s for s in snapshots if s.is_draft),
        snapshots[0] if snapshots else None,
    )

    # 🔒 Derive mode & station from snapshot state (AUTHORITATIVE)
    if active and active.status != "draft":
        mode = "read-only"
        station = "review"
    else:
        mode = "edit"
        station = "geometry"

    # 🔒 Mirror kernel block context (READ-ONLY)
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

        # Phase E visibility (derived, authoritative)
        "station": station,
        "mode": mode,

        # Snapshot state (E.3 aligned)
        "active_snapshot_id": active.id if active else None,
        "snapshot_status": active.status if active else None,
        "status": active.status if active else None,  # compatibility alias

        # Ownership resolution (read-only helper)
        "draft_ownership": (
            active.resolve_ownership(user)
            if active
            else "not_applicable"
        ),

        # Kernel truth, mirrored
        "block_reason": block_reason,
    }

@router.get("/context")
def get_studio_context(
    project_id: int | None = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_studio_state(
        project_id=project_id,
        db=db,
        user=user,
    )

