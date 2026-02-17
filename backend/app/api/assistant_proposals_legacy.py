from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.assistant_proposal import AssistantProposal
from app.models.rendered_snapshot import RenderedSnapshot
from app.services.assistant_proposal_applier import apply_assistant_proposal

router = APIRouter(prefix="/legacy/assistant-proposals", tags=["legacy"])


@router.post("/apply")
def apply_assistant_proposal_legacy(
    body: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Legacy compat endpoint for Tier 4.5 tests.

    Expected body:
      {
        "proposal_id": int,
        "snapshot_id": int,
        "confirm": bool
      }
    """
    proposal_id = body.get("proposal_id")
    snapshot_id = body.get("snapshot_id")
    confirm = body.get("confirm", False)

    if not proposal_id:
        raise HTTPException(422, "proposal_id required")
    if not snapshot_id:
        raise HTTPException(422, "snapshot_id required")

    proposal = (
        db.query(AssistantProposal)
        .filter(AssistantProposal.id == proposal_id)
        .first()
    )
    if not proposal:
        raise HTTPException(404, "Proposal not found")

    # snapshot safety (tests pass snapshot_id redundantly)
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot_id)
        .first()
    )
    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    # Ensure proposal belongs to that snapshot (prevents mismatched apply)
    if getattr(proposal, "snapshot_id", None) != snapshot.id:
        raise HTTPException(409, "Proposal ↔ snapshot mismatch")

    new_snapshot = apply_assistant_proposal(
        db=db,
        user=user,
        snapshot=snapshot,
        station=proposal.station,
        tool_name=proposal.tool,
        payload=proposal.payload or {},
        confirm=confirm,
    )

    # Test expects new_snapshot_id key
    return {"new_snapshot_id": new_snapshot.id}

