from fastapi import HTTPException
from app.services.snapshot_cloner import clone_snapshot
from app.services.audit import log_event

ALLOWED_PARAMETERS = {
    "length_offset",
    "rake_angle",
    "lateral_offset",
    "vertical_offset",
}

def apply_panel_parameters(*, db, snapshot, user, panel_id, parameters):
    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not editable")

    for key, value in parameters.items():
        if key not in ALLOWED_PARAMETERS:
            raise HTTPException(422, "Invalid parameter")
        if not isinstance(value, (int, float)):
            raise HTTPException(422, "Non-numeric parameter")

    new_snapshot = clone_snapshot(db=db, snapshot=snapshot, user=user)

    panel = next((p for p in new_snapshot.panels if p["id"] == panel_id), None)
    if not panel:
        new_snapshot.status = "failed"
        new_snapshot.error_message = "panel_not_found"
        db.commit()
        return new_snapshot

    panel.setdefault("parameters", {}).update(parameters)

    db.commit()

    log_event(
        db=db,
        user_id=user.id,
        action="panel.parameters.applied",
        resource_type="snapshot",
        resource_id=new_snapshot.id,
        extra={
            "panel_id": panel_id,
            "parameters": list(parameters.keys()),
        },
    )

    return new_snapshot

