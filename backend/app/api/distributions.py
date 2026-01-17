from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.export_job import ExportJob
from app.models.user import User

from app.services.distribution_requests import create_distribution_request
from app.services.distribution_capabilities import compute_distribution_capabilities

router = APIRouter(prefix="/distributions", tags=["distributions"])


@router.post("/requests")
def request_distribution(
    payload: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    export_id = payload.get("export_id")
    target = payload.get("target")
    options = payload.get("options", {})

    if not export_id:
        raise HTTPException(status_code=400, detail="export_id required")

    if not target:
        raise HTTPException(status_code=400, detail="target required")

    # -------------------------------------------------
    # Load export job (ONLY thing Phase N.1 requires)
    # -------------------------------------------------
    export = db.query(ExportJob).filter(ExportJob.id == export_id).first()
    if not export:
        raise HTTPException(status_code=404, detail="Export not found")

    # -------------------------------------------------
    # Export must be completed
    # -------------------------------------------------
    if export.status != "completed":
        raise HTTPException(
            status_code=409,
            detail="Export not ready for distribution",
        )

    # -------------------------------------------------
    # Compute capabilities (Phase N.1 has NO project context)
    # -------------------------------------------------
    capabilities = compute_distribution_capabilities(
        user=user,
        project=None,  # <-- INTENTIONAL
    )

    # -------------------------------------------------
    # Create request (service enforces target rules)
    # -------------------------------------------------
    return create_distribution_request(
        db=db,
        user=user,
        export=export,
        target=target,
        options=options,
        capabilities=capabilities,
    )

