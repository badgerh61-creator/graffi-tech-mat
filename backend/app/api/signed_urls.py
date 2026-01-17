from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.distribution_request import DistributionRequest
from app.services.signed_url_service import create_signed_url
from app.services.distribution_capabilities import compute_distribution_capabilities

router = APIRouter(prefix="/distributions", tags=["distributions"])


@router.post("/signed-urls")
def create_signed_url_endpoint(
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    request_id = payload.get("distribution_request_id")
    if not request_id:
        raise HTTPException(status_code=400, detail="distribution_request_id required")

    req = db.query(DistributionRequest).get(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Distribution request not found")

    # Revoked request
    if getattr(req, "revoked_at", None):
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

    result = create_signed_url(
        db=db,
        distribution_request=req,
        expires_in_hours=req.options["expires_in_hours"],
    )

    return result

