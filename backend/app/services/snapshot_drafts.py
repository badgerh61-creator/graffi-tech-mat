# backend/app/services/snapshot_drafts.py

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
# Phase U — SINGLE SOURCE OF TRUTH (DELEGATION ONLY)
# ==================================================
# ⚠️ DO NOT IMPLEMENT LOCK LOGIC HERE
# ⚠️ This file MUST NOT contain authority decisions
# ==================================================

from app.services.draft_lock_service import (
    acquire_draft_lock,
    release_draft_lock,
    require_draft_owner,
    get_draft_lock,
)


