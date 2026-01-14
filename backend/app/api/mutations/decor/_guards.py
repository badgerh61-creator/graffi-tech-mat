# app/api/mutations/decor/_guards.py

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.services.capabilities import require_capability


def require_decor_capability(db, user, project_id):
    """
    Canonical decor capability guard.
    Router-only.
    """
    try:
        require_capability(
            db=db,
            user=user,
            project_id=project_id,
            capability="canDecorateExterior",
        )
    except HTTPException:
        return JSONResponse(
            status_code=403,
            content={"error": "decor_capability_required"},
        )
    return None

