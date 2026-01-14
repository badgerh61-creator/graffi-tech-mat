from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.services.capabilities import require_capability


def require_project_capability(
    *,
    db,
    user,
    project_id,
    capability: str,
    error_code: str,
):
    """
    Canonical capability guard.
    Used by all mutation routers.
    """
    try:
        require_capability(
            db=db,
            user=user,
            project_id=project_id,
            capability=capability,
        )
    except HTTPException:
        return JSONResponse(
            status_code=403,
            content={
                "error": error_code,
                "detail": error_code,
            },
        )

    return None

