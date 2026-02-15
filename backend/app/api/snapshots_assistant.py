# backend/app/api/snapshots_assistant.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.snapshot import Snapshot
from app.models.audit import AuditLog

router = APIRouter(prefix="/snapshots", tags=["assistant"])


ALLOWED_MODES = ("inquiry", "calculation", "proposal", "review")


@router.post("/{snapshot_id}/assistant/tuning")
def assistant_tuning_endpoint(
    snapshot_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    mode = payload.get("mode")

    if mode not in ALLOWED_MODES:
        raise HTTPException(status_code=422, detail="Invalid mode")

    snapshot = db.query(Snapshot).get(snapshot_id)

    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # ✅ READ-ONLY ANALYSIS (NO MUTATION)
    response = {
        "analysis": {
            "power_to_weight": "0.120",
            "note": "Read-only assistant analysis",
        },
        "recommendations": [
            "Consider reducing vehicle weight",
            "Evaluate gear ratio adjustment",
        ],
        "confidence": 0.85,
    }

    # ✅ AUDIT EVENT (ALIGNED TO YOUR MODEL)
    audit = AuditLog(
        user_id=user.id,
        action="assistant.tuning.invoked",
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={"mode": mode},
    )

    db.add(audit)
    db.commit()

    return response

