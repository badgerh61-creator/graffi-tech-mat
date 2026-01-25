from fastapi import HTTPException
from app.models.curve_constraint import CurveConstraint
from app.services.snapshot_cloner import clone_snapshot
from app.services.audit import log_event

ALLOWED_CONSTRAINT_TYPES = {
    "horizontal",
    "vertical",
    "parallel",
    "perpendicular",
    "coincident",
    "symmetric",
    "fixed_length",
}

def add_curve_constraint(
    *,
    db,
    snapshot,
    curve,
    user,
    constraint_type,
    reference,
    params,
):
    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not editable")

    if curve is None:
        raise HTTPException(404, "Curve not found")

    if constraint_type not in ALLOWED_CONSTRAINT_TYPES:
        raise HTTPException(422, "Invalid constraint type")

    new_snapshot = clone_snapshot(db=db, snapshot=snapshot, user=user)

    constraint = CurveConstraint(
        snapshot_id=new_snapshot.id,
        curve_id=curve.id,
        type=constraint_type,
        reference=reference,
        params=params,
    )

    db.add(constraint)
    db.commit()

    log_event(
        db=db,
        user_id=user.id,
        action="curve.constraint.add",
        resource_type="constraint",
        resource_id=constraint.id,
        extra={"type": constraint_type},
    )

    return new_snapshot, constraint

