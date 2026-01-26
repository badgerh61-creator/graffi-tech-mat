from fastapi import HTTPException
from app.services.panel_parameters import apply_panel_parameters

def apply_panel_parameters_endpoint(db, snapshot, user, payload):
    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(403)

    return apply_panel_parameters(
        db=db,
        snapshot=snapshot,
        user=user,
        panel_id=payload["panel_id"],
        parameters=payload["parameters"],
    )

