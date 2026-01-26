from fastapi import HTTPException
from app.services.surface_generation_service import (
    generate_surfaces_for_snapshot,
)

def generate_surfaces_endpoint(db, snapshot, user):
    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(403)

    return generate_surfaces_for_snapshot(
        db=db,
        snapshot=snapshot,
        user=user,
    )

