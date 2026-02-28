# backend/app/services/draft_workspace_service.py
from __future__ import annotations

from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session


def _require_lock_services() -> tuple:
    """
    Phase U integration.
    Fail-closed if lock service isn't present.
    """
    try:
        from app.services.draft_lock_service import (
            require_draft_owner,
            acquire_draft_lock,
            release_draft_lock,
        )
        return require_draft_owner, acquire_draft_lock, release_draft_lock
    except Exception:
        raise HTTPException(403, "Draft lock services unavailable")


def _audit_if_available(*, db: Session, user_id: int, action: str, resource_id: int, extra: dict) -> None:
    try:
        from app.services.audit import log_event
    except Exception:
        return

    log_event(
        db=db,
        user_id=user_id,
        action=action,
        resource_type="snapshot",
        resource_id=resource_id,
        extra=extra,
    )


def _clone_snapshot_as_child_draft(*, db: Session, snapshot, user_id: int) -> object:
    """
    Additive-safe clone:
    - copies common fields if present
    - sets status="draft"
    - sets parent_snapshot_id if field exists
    - sets created_by / owner_user_id if schema requires it (rendered_snapshots.created_by is NOT NULL)
    """
    SnapshotModel = snapshot.__class__

    child = SnapshotModel(
        project_id=getattr(snapshot, "project_id", None),
        scene_state_hash=getattr(snapshot, "scene_state_hash", None),
        render_profile=getattr(snapshot, "render_profile", "default"),
        image_url=getattr(snapshot, "image_url", None),
        engine_version=getattr(snapshot, "engine_version", None),
        status="draft",
        error_message=None,
    )

    # Parent linkage (if supported)
    if hasattr(child, "parent_snapshot_id"):
        setattr(child, "parent_snapshot_id", getattr(snapshot, "id"))

    # Copy authoritative states if present
    if hasattr(child, "body_state"):
        setattr(child, "body_state", getattr(snapshot, "body_state", None))
    if hasattr(child, "decor_state"):
        setattr(child, "decor_state", getattr(snapshot, "decor_state", None))
    if hasattr(child, "tuning_state"):
        setattr(child, "tuning_state", getattr(snapshot, "tuning_state", None))

    # Required authorship / ownership fields (fail-safe: only set if column exists)
    if hasattr(child, "created_by"):
        setattr(child, "created_by", int(user_id))
    if hasattr(child, "owner_user_id"):
        setattr(child, "owner_user_id", int(user_id))

    db.add(child)
    db.commit()
    db.refresh(child)
    return child


def start_edit(*, db: Session, snapshot, user) -> int:
    """
    Returns draft_snapshot_id.
    If completed -> clone child draft + lock it.
    If draft -> lock same snapshot.
    """
    require_draft_owner, acquire_draft_lock, _ = _require_lock_services()

    user_id = getattr(user, "id", None)
    if not user_id:
        raise HTTPException(401, "Not authenticated")
    user_id = int(user_id)

    status = getattr(snapshot, "status", None)
    if status not in ("draft", "completed"):
        raise HTTPException(409, "Snapshot status not eligible for edit")

    parent_id = int(getattr(snapshot, "id"))

    # If completed: clone -> lock cloned draft -> return draft id
    if status == "completed":
        draft = _clone_snapshot_as_child_draft(db=db, snapshot=snapshot, user_id=user_id)

        # IMPORTANT: lock service expects snapshot + user (not ids)
        acquire_draft_lock(db=db, snapshot=draft, user=user)
        require_draft_owner(db=db, snapshot=draft, user=user)

        draft_id = int(getattr(draft, "id"))

        _audit_if_available(
            db=db,
            user_id=user_id,
            action="studio.mode.start_edit",
            resource_id=draft_id,
            extra={"parent_snapshot_id": parent_id, "draft_snapshot_id": draft_id},
        )
        return draft_id

    # status == "draft": lock existing draft -> enforce ownership -> return same id
    acquire_draft_lock(db=db, snapshot=snapshot, user=user)
    require_draft_owner(db=db, snapshot=snapshot, user=user)

    draft_id = int(getattr(snapshot, "id"))

    _audit_if_available(
        db=db,
        user_id=user_id,
        action="studio.mode.start_edit",
        resource_id=draft_id,
        extra={
            "parent_snapshot_id": getattr(snapshot, "parent_snapshot_id", None),
            "draft_snapshot_id": draft_id,
        },
    )
    return draft_id


def complete_draft(*, db: Session, snapshot, user) -> int:
    """
    Draft -> completed, lock required.
    Returns completed_snapshot_id (same id).
    """
    require_draft_owner, _, _ = _require_lock_services()

    user_id = getattr(user, "id", None)
    if not user_id:
        raise HTTPException(401, "Not authenticated")
    user_id = int(user_id)

    if getattr(snapshot, "status", None) != "draft":
        raise HTTPException(409, "Only draft snapshots can be completed")

    require_draft_owner(db=db, snapshot=snapshot, user=user)

    setattr(snapshot, "status", "completed")
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    sid = int(getattr(snapshot, "id"))

    _audit_if_available(
        db=db,
        user_id=user_id,
        action="studio.mode.complete_draft",
        resource_id=sid,
        extra={"draft_snapshot_id": sid, "completed_snapshot_id": sid},
    )
    return sid


def discard_draft(*, db: Session, snapshot, user) -> int:
    """
    Discard a draft workspace:
    - lock required
    - best-effort release lock
    - return parent_snapshot_id if available else same
    """
    require_draft_owner, _, release_draft_lock = _require_lock_services()

    user_id = getattr(user, "id", None)
    if not user_id:
        raise HTTPException(401, "Not authenticated")
    user_id = int(user_id)

    if getattr(snapshot, "status", None) != "draft":
        raise HTTPException(409, "Only draft snapshots can be discarded")

    require_draft_owner(db=db, snapshot=snapshot, user=user)

    parent_id: Optional[int] = None
    if hasattr(snapshot, "parent_snapshot_id"):
        parent_id = getattr(snapshot, "parent_snapshot_id") or None

    try:
        # IMPORTANT: release expects snapshot + user (not ids)
        release_draft_lock(db=db, snapshot=snapshot, user=user)
    except Exception:
        pass

    sid = int(getattr(snapshot, "id"))

    _audit_if_available(
        db=db,
        user_id=user_id,
        action="studio.mode.discard_draft",
        resource_id=sid,
        extra={"draft_snapshot_id": sid, "parent_snapshot_id": parent_id},
    )

    return int(parent_id or sid)
