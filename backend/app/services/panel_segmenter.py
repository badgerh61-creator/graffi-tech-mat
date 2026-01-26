from fastapi import HTTPException
from app.services.audit import log_event


def segment_panels(*, db, snapshot, user, panels):
    if snapshot.status != "draft":
        raise HTTPException(status_code=409, detail="Snapshot not editable")

    # 🔒 AUTHORITATIVE CLONE (Phase K invariant)
    new_snapshot = snapshot.clone_for_mutation(created_by=user.id)
    db.add(new_snapshot)
    db.flush()

    surfaces_by_id = {s["id"]: s for s in new_snapshot.surfaces}

    created_panels = []

    for panel in panels:
        for sid in panel["surface_ids"]:
            if sid not in surfaces_by_id:
                new_snapshot.status = "failed"
                new_snapshot.error_message = "surface_not_found"
                db.commit()
                return new_snapshot

        created_panels.append({
            "id": f"panel-{len(created_panels) + 1}",
            "type": panel["type"],
            "label": panel.get("label"),
            "surface_ids": panel["surface_ids"],
        })

    new_snapshot.panels = created_panels
    db.commit()

    log_event(
        db=db,
        user_id=user.id,
        action="panel.segmented",
        resource_type="snapshot",
        resource_id=new_snapshot.id,
        extra={"panel_count": len(created_panels)},
    )

    return new_snapshot

