from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.rendered_snapshot import RenderedSnapshot
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
            db.query(RenderedSnapshot.project_id)
            .order_by(RenderedSnapshot.created_at.desc())
            .limit(1)
            .scalar()
        )

    snapshots = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.project_id == project_id)
        .order_by(RenderedSnapshot.created_at.desc())
        .all()
    )

    # 🔒 Prefer active DRAFT snapshot
    active = next(
        (s for s in snapshots if s.is_draft),
        snapshots[0] if snapshots else None,
    )

    # 🔒 Local derivation of mode & station (Phase E only)
    if active and active.status != "draft":
        mode = "read-only"
        station = "review"
    else:
        mode = "edit"
        station = "geometry"

    # 🔒 Mirror kernel block context (READ-ONLY)
    blocked = None
    if active is not None:
        blocked = get_blocked_execution_context(
            db=db,
            user=user,
            snapshot=active,
        )

    # Phase E.1 invariant: never silently drop block context
    if active is not None and blocked is None:
        blocked = {
            "code": "snapshot.locked",
            "reason": "Snapshot is not editable",
        }

    block_reason = (
        {
            "code": blocked.get("code"),
            "reason": blocked.get("reason"),
        }
        if blocked
        else None
    )

    return {
        "project_id": project_id,

        # Phase E visibility
        "station": station,
        "mode": mode,

        # Snapshot state
        "active_snapshot_id": active.id if active else None,
        "snapshot_status": active.status if active else None,
        "status": active.status if active else None,  # compatibility alias

        # ✅ AUTHORITATIVE ownership
        "draft_ownership": (
            active.resolve_ownership(user)
            if active
            else "not_applicable"
        ),

        # Kernel truth
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

