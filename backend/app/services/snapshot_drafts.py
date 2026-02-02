from datetime import datetime
from fastapi import HTTPException

from app.models.rendered_snapshot import RenderedSnapshot as Snapshot


# ==================================================
# Canonical draft creation (Phase 4.x)
# ==================================================

def create_draft_snapshot(db, *, snapshot, user):
    if snapshot is None:
        raise HTTPException(404, "Snapshot not found")

    if user.role == "viewer":
        raise HTTPException(403, "Viewers cannot create draft snapshots")

    if snapshot.status != "completed":
        raise HTTPException(409, "Only completed snapshots can be drafted")

    existing = (
        db.query(Snapshot)
        .filter(
            Snapshot.project_id == snapshot.project_id,
            Snapshot.status == "draft",
        )
        .first()
    )

    if existing:
        raise HTTPException(409, "Draft snapshot already exists")

    draft = Snapshot(
        project_id=snapshot.project_id,
        scene_state_hash=snapshot.scene_state_hash,
        render_profile=snapshot.render_profile,
        engine_version=snapshot.engine_version,
        status="draft",
        parent_snapshot_id=snapshot.id,
        created_by=user.id,
        created_at=datetime.utcnow(),
    )

    db.add(draft)
    db.commit()
    db.refresh(draft)

    return draft


# ==================================================
# Legacy compatibility entrypoints
# ==================================================

def create_draft_from_completed(db, *, snapshot, user):
    return create_draft_snapshot(db=db, snapshot=snapshot, user=user)


def autosave_draft(db, *, snapshot, new_state_hash, user):
    if snapshot is None:
        raise HTTPException(404, "Snapshot not found")

    if snapshot.status != "draft":
        raise HTTPException(409, "Only draft snapshots can be autosaved")

    snapshot.scene_state_hash = new_state_hash
    snapshot.updated_at = datetime.utcnow()

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot


autosave_draft_snapshot = autosave_draft


# ==================================================
# Phase U kernel primitive (AUTHORITATIVE)
# ==================================================

def acquire_draft_lock(*, db, snapshot, user):
    """
    Phase U kernel primitive.

    Establishes single-writer ownership for a draft snapshot.
    """

    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot is not draft")

    # If already owned by another user → block
    if snapshot.owner_user_id not in (None, user.id):
        raise HTTPException(409, "Draft locked by another user")

    snapshot.owner_user_id = user.id
    snapshot.locked_at = datetime.utcnow()

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot


def release_draft_lock(*, db, snapshot, user):
    """
    Releases draft ownership.
    Idempotent and safe.
    """

    if snapshot.status != "draft":
        return snapshot

    if snapshot.owner_user_id != user.id:
        return snapshot

    snapshot.owner_user_id = None
    snapshot.locked_at = None

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot


# ==================================================
# Phase U — Compatibility re-exports (DO NOT REMOVE)
# ==================================================

from app.services.draft_lock_service import require_draft_owner

