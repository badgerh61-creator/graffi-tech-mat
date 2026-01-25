from fastapi import HTTPException
from datetime import datetime

from app.models.curve import Curve
from app.services.snapshot_cloner import clone_snapshot
from app.services.audit import log_event

ALLOWED_CURVE_TYPES = {"line", "arc", "cubic_bezier"}


def create_curve(
    *,
    db,
    snapshot,
    user,
    curve_type,
    reference_plane_id,
    params,
    constraints,
):
    # 🔒 Lifecycle enforcement
    if snapshot.status != "draft":
        raise HTTPException(status_code=409, detail="Snapshot not editable")

    # 🔒 Type enforcement
    if curve_type not in ALLOWED_CURVE_TYPES:
        raise HTTPException(status_code=422, detail="Invalid curve type")

    # 🔒 Reference frame required
    if not reference_plane_id:
        raise HTTPException(status_code=400, detail="Reference plane required")

    # 🔁 Immutable snapshot cloning
    new_snapshot = clone_snapshot(
        db=db,
        snapshot=snapshot,
        user=user,
    )

    curve = Curve(
        snapshot_id=new_snapshot.id,
        type=curve_type,
        reference_plane_id=reference_plane_id,
        params=params,
        constraints=constraints or [],
    )

    db.add(curve)
    db.commit()
    db.refresh(curve)

    # 🧾 Audit is the source of truth
    log_event(
        db=db,
        user_id=user.id,
        action="curve.create",
        resource_type="curve",
        resource_id=curve.id,
        extra={
            "curve_type": curve_type,
            "snapshot_id": new_snapshot.id,
        },
    )

    return new_snapshot, curve

