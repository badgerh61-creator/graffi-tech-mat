from fastapi import HTTPException
from app.services.panel_segmenter import segment_panels

def segment_panels_endpoint(db, snapshot, user, panels):
    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(403)

    return segment_panels(
        db=db,
        snapshot=snapshot,
        user=user,
        panels=panels,
    )

