from __future__ import annotations

from typing import Any, Dict

from fastapi import HTTPException
from sqlalchemy.orm import Session

ALLOWED_TOOLS = {"TRANSLATE", "ROTATE", "SCALE"}


def _require_draft_lock_if_available(*, db: Session, snapshot_id: int, user_id: int) -> None:
    """
    Phase U enforcement.
    If your repo has require_draft_owner(), we call it.
    If it doesn't exist yet in some deployments, we fail closed with 403.
    """
    try:
        from app.services.draft_lock_service import require_draft_owner
    except Exception:
        raise HTTPException(403, "Draft lock service unavailable")

    require_draft_owner(db=db, snapshot_id=snapshot_id, user_id=user_id)


def _audit_if_available(
    *,
    db: Session,
    user_id: int,
    new_snapshot_id: int,
    parent_snapshot_id: int,
    station: str,
    tool: str,
    target_id: str,
    payload: Dict[str, Any] | None = None,
) -> None:
    """
    Tier 7.3 + 7.4 audit enrichment.
    """
    try:
        from app.services.audit import log_event
    except Exception:
        return

    p = payload or {}

    extra = {
        "parent_snapshot_id": parent_snapshot_id,
        "station": station,
        "tool": tool,
        "target_id": target_id,
        "snap": bool(p.get("snap", False)),
        "axis_lock": p.get("axis_lock", "xyz"),
        "drag_source": p.get("drag_source"),
    }

    if p.get("frame_id") is not None:
        extra["frame_id"] = p.get("frame_id")

    if p.get("snap_step") is not None:
        extra["snap_step"] = p.get("snap_step")

    log_event(
        db=db,
        user_id=user_id,
        action="snapshot.transform",
        resource_type="snapshot",
        resource_id=new_snapshot_id,
        extra=extra,
    )


def _copy_if_present(dst, src, field: str) -> None:
    if hasattr(dst, field) and hasattr(src, field):
        try:
            setattr(dst, field, getattr(src, field))
        except Exception:
            pass


def _set_if_present(obj, field: str, value) -> None:
    if hasattr(obj, field):
        try:
            setattr(obj, field, value)
        except Exception:
            pass


def execute_transform_tool(
    *,
    db: Session,
    snapshot,
    user,
    station: str,
    tool: str,
    payload: Dict[str, Any],
):
    """
    Tier 7.x governed transform execution.

    HARD RULES:
    - draft-only
    - lock required
    - new child draft snapshot (no mutation)
    - audit event emitted
    """

    tool = (tool or "").upper().strip()
    if tool not in ALLOWED_TOOLS:
        raise HTTPException(422, "Invalid tool")

    if getattr(snapshot, "status", None) != "draft":
        raise HTTPException(409, "Only draft snapshots may be transformed")

    user_id = getattr(user, "id", None)
    if not user_id:
        raise HTTPException(401, "Not authenticated")

    _require_draft_lock_if_available(
        db=db,
        snapshot_id=snapshot.id,
        user_id=user_id,
    )

    if not isinstance(payload, dict):
        raise HTTPException(422, "Invalid payload")

    target_id = payload.get("target_id")
    if not target_id or not isinstance(target_id, str):
        raise HTTPException(422, "payload.target_id required")

    # -------------------------------------------------
    # Tier 7.3: merge payload.params upward
    # -------------------------------------------------
    params = payload.get("params")
    if isinstance(params, dict):
        payload = {**payload, **params}

    # -------------------------------------------------
    # Tier 7.3 + 7.4: normalize (snapping + axis locks)
    # -------------------------------------------------
    from app.services.transform_payload_normalizer import normalize_transform_payload

    payload = normalize_transform_payload(payload=payload)

    SnapshotModel = snapshot.__class__

    # -------------------------------------------------
    # Immutable clone (new child draft)
    # -------------------------------------------------
    new_snapshot = SnapshotModel(
        project_id=getattr(snapshot, "project_id"),
        scene_state_hash=getattr(snapshot, "scene_state_hash"),
        render_profile=getattr(snapshot, "render_profile", "default"),
        image_url=getattr(snapshot, "image_url", None),
        engine_version=getattr(snapshot, "engine_version", None),
        status="draft",
        error_message=None,
    )

    # Parent linkage (if field exists)
    _set_if_present(new_snapshot, "parent_snapshot_id", snapshot.id)

    # Required author fields
    if hasattr(new_snapshot, "created_by"):
        _set_if_present(new_snapshot, "created_by", user_id)

    if hasattr(new_snapshot, "owner_user_id"):
        _set_if_present(new_snapshot, "owner_user_id", user_id)

    # Safe field propagation
    _copy_if_present(new_snapshot, snapshot, "deterministic_key")
    _copy_if_present(new_snapshot, snapshot, "is_corrupted")
    _copy_if_present(new_snapshot, snapshot, "locked_at")

    # Optional metadata
    _set_if_present(new_snapshot, "last_tool", tool)

    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)

    # -------------------------------------------------
    # Audit
    # -------------------------------------------------
    _audit_if_available(
        db=db,
        user_id=user_id,
        new_snapshot_id=new_snapshot.id,
        parent_snapshot_id=snapshot.id,
        station=station,
        tool=tool,
        target_id=target_id,
        payload=payload,
    )

    return new_snapshot
