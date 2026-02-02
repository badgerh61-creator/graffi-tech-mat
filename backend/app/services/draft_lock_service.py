# backend/app/services/draft_lock_service.py

from datetime import datetime
from fastapi import HTTPException

from app.services.audit import log_event


def acquire_draft_lock(*, db, snapshot, user):
    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not draft")

    if snapshot.owner_user_id not in (None, user.id):
        raise HTTPException(409, "Draft already locked")

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

    if snapshot.owner_user_id != user.id and not force:
        raise HTTPException(403, "Not lock owner")

    previous_owner_id = snapshot.owner_user_id

    snapshot.owner_user_id = None
    snapshot.locked_at = None

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    log_event(
        db=db,
        user_id=user.id,
        action="draft.lock.forced" if force else "draft.lock.released",
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={
            "previous_owner_id": previous_owner_id,
            "forced": force,
            "project_id": snapshot.project_id,
        },
    )

    return snapshot


def get_draft_lock(*, snapshot):
    """
    Phase U.2 — Compatibility accessor (tests & kernel expect this)
    """
    return snapshot.owner_user_id


def require_draft_owner(*, db, snapshot, user):
    """
    Phase U.2 — Authoritative ownership check (FROZEN)
    """

    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot is not a draft")

    if snapshot.owner_user_id != user.id:
        raise HTTPException(403, "User does not own draft")

    return snapshot


# ==================================================
# Phase U.2 COMPATIBILITY ADAPTER — DO NOT REMOVE
# ==================================================

class _DraftLockView:
    """
    Compatibility view for legacy Phase U.2 / U.4 tests.
    This is NOT a persisted model.
    """
    def __init__(self, snapshot):
        self.snapshot_id = snapshot.id
        self.user_id = snapshot.owner_user_id


def get_draft_lock(*, db, snapshot):
    """
    Phase U.2 — Legacy accessor.

    Returns a lock-like object if locked,
    otherwise None.
    """
    if snapshot.owner_user_id is None:
        return None

    return _DraftLockView(snapshot)

