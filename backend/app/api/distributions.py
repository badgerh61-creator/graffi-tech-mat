from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.export_job import ExportJob
from app.models.user import User
from app.models.distribution_request import DistributionRequest

from app.services.distribution_requests import create_distribution_request
from app.services.distribution_capabilities import compute_distribution_capabilities
from app.services.signed_url_service import create_signed_url

router = APIRouter(prefix="/distributions", tags=["distributions"])


# ============================================================
# 📦 Phase N.1 — Distribution Requests
# ============================================================

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

    export = db.query(ExportJob).filter(ExportJob.id == export_id).first()
    if not export:
        raise HTTPException(status_code=404, detail="Export not found")

    if export.status != "completed":
        raise HTTPException(
            status_code=409,
            detail="Export not ready for distribution",
        )

    capabilities = compute_distribution_capabilities(
        user=user,
        project=None,  # Phase N.1 has no project context
    )

    req = create_distribution_request(
        db=db,
        user=user,
        export=export,
        target=target,
        options=options,
        capabilities=capabilities,
    )

    # ✅ Phase N.1 RESPONSE CONTRACT
    return {
        "id": req.id,
        "status": "accepted",
        "target": req.target,
    }


# ============================================================
# 🔗 Phase N.2 — Signed URL Delivery
# ============================================================

@router.post("/signed-urls")
def create_signed_url_endpoint(
    payload: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    request_id = payload.get("distribution_request_id")
    if not request_id:
        raise HTTPException(status_code=400, detail="distribution_request_id required")

    req = db.query(DistributionRequest).get(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Distribution request not found")

    if req.revoked_at is not None:
        raise HTTPException(status_code=410, detail="Distribution request revoked")

    export = req.export
    if export.status != "completed":
        raise HTTPException(status_code=409, detail="Export not completed")

    caps = compute_distribution_capabilities(
        user=user,
        project=export.project,
    )

    if not caps["canCreatePublicLinks"]:
        raise HTTPException(status_code=403, detail="Not permitted")

    # ✅ Phase N.2 RESPONSE CONTRACT
    return create_signed_url(
        db=db,
        distribution_request=req,
        expires_in_hours=req.options["expires_in_hours"],
    )

