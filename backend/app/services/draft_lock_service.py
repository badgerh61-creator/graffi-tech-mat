from fastapi import HTTPException

from app.models.draft_lock import DraftLock
from app.services.audit import log_event


def acquire_draft_lock(*, db, snapshot, user):
    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not draft")

    existing = (
        db.query(DraftLock)
        .filter_by(snapshot_id=snapshot.id)
        .first()
    )

    if existing:
        raise HTTPException(409, "Draft already locked")

    lock = DraftLock(
        snapshot_id=snapshot.id,
        user_id=user.id,
    )

    db.add(lock)
    db.commit()

    # ✅ AUDIT — compliant with frozen contract
    log_event(
        db=db,
        user_id=user.id,
        action="draft.lock.acquired",
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={
            "project_id": snapshot.project_id,
        },
    )

    return lock


def release_draft_lock(*, db, snapshot, user, force=False):
    lock = (
        db.query(DraftLock)
        .filter_by(snapshot_id=snapshot.id)
        .first()
    )

    if not lock:
        return

    if lock.user_id != user.id and not force:
        raise HTTPException(403, "Not lock owner")

    previous_owner_id = lock.user_id

    db.delete(lock)
    db.commit()

    # ✅ AUDIT — compliant with frozen contract
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


def get_draft_lock(*, db, snapshot):
    return (
        db.query(DraftLock)
        .filter_by(snapshot_id=snapshot.id)
        .first()
    )

