# backend/app/services/conflict_resolver.py

from fastapi import HTTPException, status

from app.services.audit import log_event
from app.services.conflict_detector import detect_conflict
from app.models.rendered_snapshot import RenderedSnapshot


def resolve_conflict(*, db, snapshot: RenderedSnapshot, user, strategy: str):
    """
    Phase U.3 — Conflict Resolution (AUTHORITATIVE)
    """

    conflict = detect_conflict(db=db, snapshot=snapshot, user=user)

    if not conflict.is_conflicted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No conflict to resolve",
        )

    # --------------------------------------------------
    # Strategy: ABANDON
    # --------------------------------------------------
    if strategy == "abandon":
        snapshot.status = "abandoned"
        db.commit()

    # --------------------------------------------------
    # Strategy: REBASE
    # --------------------------------------------------
    elif strategy == "rebase":
        latest = (
            db.query(RenderedSnapshot)
            .filter(
                RenderedSnapshot.project_id == snapshot.project_id,
                RenderedSnapshot.status == "completed",
            )
            .order_by(RenderedSnapshot.created_at.desc())
            .first()
        )

        if not latest:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No completed snapshot to rebase onto",
            )

        # Fork new draft
        rebased = RenderedSnapshot(
            project_id=snapshot.project_id,
            parent_snapshot_id=latest.id,
            scene_state_hash=snapshot.scene_state_hash,
            render_profile=snapshot.render_profile,
            engine_version=snapshot.engine_version,
            deterministic_key=snapshot.deterministic_key,
            status="draft",
            owner_user_id=user.id,
            created_by=user.id,
        )

        db.add(rebased)
        db.commit()
        snapshot = rebased

    # --------------------------------------------------
    # Strategy: FORCE (ADMIN ONLY)
    # --------------------------------------------------
    elif strategy == "force":
        if user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin only",
            )
        # Force means: do nothing, allow continuation

    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid resolution strategy",
        )

    # --------------------------------------------------
    # Audit
    # --------------------------------------------------
    log_event(
        db=db,
        user_id=user.id,
        action="draft.conflict.resolved",
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={"strategy": strategy},
    )

    return snapshot


# Compatibility shim (used by earlier phases / tests)
def resolve_conflict_and_fork(*, db, snapshot, user):
    return resolve_conflict(
        db=db,
        snapshot=snapshot,
        user=user,
        strategy="rebase",
    )

