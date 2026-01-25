from fastapi import HTTPException
from app.services.curve_constraints import add_curve_constraint

def add_constraint_endpoint(db, snapshot, curve, user, payload):
    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(403)

    return add_curve_constraint(
        db=db,
        snapshot=snapshot,
        curve=curve,
        user=user,
        constraint_type=payload["type"],
        reference=payload.get("reference"),
        params=payload.get("params", {}),
    )

