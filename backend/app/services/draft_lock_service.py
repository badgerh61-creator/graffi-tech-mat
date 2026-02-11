# backend/app/services/draft_lock_service.py
from datetime import datetime
from fastapi import HTTPException

from app.models.rendered_snapshot import RenderedSnapshot
from app.services.audit import log_event


def acquire_draft_lock(*, db, snapshot, user):
    """
    Phase U — AUTHORITATIVE draft lock acquisition

    Invariants:
    - Lock acquisition establishes ownership if unlocked
    - Ownership is transferable via lock
    - Conflicts dominate
    """

    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not draft")

    # 👁 Viewers never lock
    if user.role == "viewer":
        return snapshot

    # 🔥 If locked by someone else → block
    if snapshot.locked_at is not None and snapshot.owner_user_id != user.id:
        raise HTTPException(409, "Draft locked by another user")

    # ✅ ESTABLISH AUTHORITY ON LOCK
    snapshot.owner_user_id = user.id
    snapshot.locked_at = datetime.utcnow()

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    log_event(
        db=db,
        user_id=user.id,
        action="draft.lock.acquired",
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={"project_id": snapshot.project_id},
    )

    return snapshot


def release_draft_lock(*, db, snapshot, user, force=False):
    if snapshot.status != "draft":
        return snapshot

    if snapshot.locked_at is None:
        return snapshot

    if snapshot.owner_user_id != user.id and not force:
        raise HTTPException(403, "Not lock owner")

    previous_owner_id = snapshot.owner_user_id

    # 🔓 FULL UNLOCK (Phase U contract)
    snapshot.locked_at = None
    snapshot.owner_user_id = None

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    log_event(
        db=db,
        user_id=user.id,
        action="draft.lock.released",
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={
            "previous_owner_id": previous_owner_id,
            "forced": force,
            "project_id": snapshot.project_id,
        },
    )

    return snapshot


# ==================================================
# Phase U.2 compatibility
# ==================================================

class _DraftLockView:
    def __init__(self, snapshot):
        self.snapshot_id = snapshot.id
        self.user_id = snapshot.owner_user_id


def get_draft_lock(*, db=None, snapshot):
    if snapshot.owner_user_id is None:
        return None
    return _DraftLockView(snapshot)


def require_draft_owner(*, db, snapshot, user):
    """
    Phase U — AUTHORITATIVE ownership check

    Rules:
    - Snapshot must be draft
    - Ownership is resolved from DB (not in-memory)
    - Read views never block the owner
    """

    fresh = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot.id)
        .with_for_update()
        .one()
    )

    if fresh.status != "draft":
        raise HTTPException(409, "Snapshot is not a draft")

    if fresh.owner_user_id is None:
        raise HTTPException(409, "Draft has no owner")

    if fresh.owner_user_id != user.id:
        raise HTTPException(403, "Not draft owner")

    return fresh

