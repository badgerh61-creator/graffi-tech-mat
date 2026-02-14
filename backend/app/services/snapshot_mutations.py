from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

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

    # =====================================================
    # Load authoritative row
    # =====================================================

    fresh = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot.id)
        .one()
    )

    # =====================================================
    # Lifecycle
    # =====================================================

    if fresh.status != "draft":
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Snapshot not editable",
        )

    # =====================================================
    # Ownership
    # =====================================================

    if fresh.owner_user_id != user.id:
        audit.log_event(
            db=db,
            user_id=user.id,
            action="snapshot.access_denied",
            resource_type="snapshot",
            resource_id=fresh.id,
            extra={"reason": "not_owner"},
        )
        db.flush()

        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Not draft owner",
        )

    # =====================================================
    # Operation validation
    # =====================================================

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

    # =====================================================
    # Fork immutable draft (SINGLE WRITER GUARANTEE)
    # =====================================================

    new_snapshot = RenderedSnapshot(
        project_id=fresh.project_id,
        scene_state_hash=fresh.scene_state_hash,
        render_profile=fresh.render_profile,
        engine_version=fresh.engine_version,
        status="draft",
        parent_snapshot_id=fresh.id,
        created_by=user.id,
        owner_user_id=user.id,
        created_at=datetime.utcnow(),
    )

    new_snapshot._apply_transform_internal(
        target_id=target_id,
        operation=operation,
        params=params,
    )

    try:
        db.add(new_snapshot)
        db.commit()
        db.refresh(new_snapshot)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Concurrent modification",
        )

    # =====================================================
    # Audit success
    # =====================================================

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
            "parent_snapshot_id": fresh.id,
        },
    )

    return new_snapshot


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

