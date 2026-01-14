# app/api/jobs/_guards.py

from fastapi.responses import JSONResponse
from app.crud import require_model_role


def require_job_execution_role(db, user, model):
    """
    Canonical job execution guard.
    Router-only. Normalized error shape.
    """
    try:
        require_model_role(
            db=db,
            user=user,
            model=model,
            min_role="editor",
        )
    except PermissionError:
        return JSONResponse(
            status_code=403,
            content={
                "error": "job_permission_required",
                "detail": "job_permission_required",
            },
        )

    return None

