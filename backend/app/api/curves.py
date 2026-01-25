from fastapi import HTTPException

def create_curve_endpoint(db, snapshot, user, payload):
    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(403)

    return create_curve(
        db=db,
        snapshot=snapshot,
        user=user,
        curve_type=payload["type"],
        reference_plane_id=payload["reference_plane_id"],
        params=payload["params"],
        constraints=payload.get("constraints", []),
    )

