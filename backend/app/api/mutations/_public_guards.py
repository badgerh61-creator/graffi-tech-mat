# app/api/mutations/_public_guards.py

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.services.capabilities import require_capability


def require_public_decor_capability(db, user, project_id):
    """
    Canonical public-router capability guard.

    Used for public snapshot activation and similar
    non-mutation but state-affecting endpoints.
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

