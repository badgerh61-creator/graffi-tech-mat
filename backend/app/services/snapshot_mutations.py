from datetime import datetime
from fastapi import HTTPException, status

from app.models.rendered_snapshot import RenderedSnapshot
from app.services import audit

ALLOWED_OPERATIONS = {"translate", "rotate", "scale"}


def apply_mutation(
    *,
    db,
    snapshot,
    user,
    operation: str,
    target_id: str,
    params: dict,
):
    if snapshot is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Snapshot not found")

    if snapshot.status != "draft":
        raise HTTPException(status.HTTP_409_CONFLICT, "Snapshot not editable")

    if operation not in ALLOWED_OPERATIONS:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Invalid transform operation",
        )

    if not target_id:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Missing target_id",
        )

    # 🔁 Create new draft snapshot
    new_snapshot = RenderedSnapshot(
        project_id=snapshot.project_id,
        scene_state_hash=snapshot.scene_state_hash,
        render_profile=snapshot.render_profile,
        engine_version=snapshot.engine_version,
        status="draft",
        parent_snapshot_id=snapshot.id,
        created_by=user.id,
        created_at=datetime.utcnow(),
    )

    # 🔒 Deterministic placeholder hash
    new_snapshot.scene_state_hash = (
        f"{snapshot.scene_state_hash}|{operation}|{target_id}|{params}"
    )

    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)

    # 🧾 AUDIT (Phase 5.1 contract)
    audit.log_event(
        db=db,
        user_id=user.id,
        action="snapshot.transform",
        resource_type="snapshot",
        resource_id=new_snapshot.id,
        extra={
            "operation": operation,
            "target_id": target_id,
            "params": params,
            "parent_snapshot_id": snapshot.id,
        },
    )

    return new_snapshot


# =====================================
# 🔁 TEST-COMPATIBILITY ALIAS
# =====================================

def apply_transform(
    *,
    db,
    snapshot,
    user,
    operation,
    target_id,
    params,
):
    return apply_mutation(
        db=db,
        snapshot=snapshot,
        user=user,
        operation=operation,
        target_id=target_id,
        params=params,
    )

