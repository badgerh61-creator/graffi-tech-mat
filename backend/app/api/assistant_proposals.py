# backend/app/api/assistant_proposals.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.services.audit import log_event

from app.models.rendered_snapshot import RenderedSnapshot
from app.models.assistant_proposal import AssistantProposal

from app.services.assistant_proposal_bridge import proposal_to_tool_request
from app.services.studio_kernel_executor import evaluate_tool_invocation
from app.services.assistant_proposal_applier import apply_assistant_proposal


# ✅ MUST match tests: "/assistant/proposals/apply"
router = APIRouter(prefix="/assistant/proposals", tags=["assistant-proposals"])


def _load_snapshot_or_404(db: Session, snapshot_id: int) -> RenderedSnapshot:
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot_id)
        .first()
    )
    if not snapshot:
        raise HTTPException(404, "Snapshot not found")
    return snapshot


def _load_proposal_or_404(db: Session, proposal_id: int) -> AssistantProposal:
    proposal = (
        db.query(AssistantProposal)
        .filter(AssistantProposal.id == proposal_id)
        .first()
    )
    if not proposal:
        raise HTTPException(404, "Proposal not found")
    return proposal


@router.post("/evaluate")
def evaluate_assistant_proposal(
    body: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Tier 4.5 — Read-only evaluation endpoint.

    Supports:
      A) { "snapshot_id": 123, "proposal": {...} }
      B) { "snapshot_id": 123, "proposal_id": 9 }
    """
    snapshot_id = body.get("snapshot_id")
    if not snapshot_id:
        raise HTTPException(422, "snapshot_id required")

    snapshot = _load_snapshot_or_404(db, int(snapshot_id))

    proposal_id = body.get("proposal_id")
    if proposal_id:
        p = _load_proposal_or_404(db, int(proposal_id))
        proposal = {"station": p.station, "tool": p.tool, "payload": p.payload or {}}
    else:
        proposal = body.get("proposal") or {}

    tool_req = proposal_to_tool_request(proposal=proposal)

    decision = evaluate_tool_invocation(
        user=user,
        snapshot=snapshot,
        station=tool_req["station"],
        tool=tool_req["tool"],
        payload=tool_req["payload"],
    )

    log_event(
        db,
        user_id=getattr(user, "id", None),
        action="assistant.proposal.evaluated",
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={
            "station": tool_req["station"],
            "tool": tool_req["tool"],
            "allowed": decision.allowed,
            "reason": decision.reason,
            "mode": decision.mode,
            "proposal_id": int(proposal_id) if proposal_id else None,
        },
    )

    return {
        "allowed": decision.allowed,
        "reason": decision.reason,
        "mode": decision.mode,
        "station": tool_req["station"],
        "tool": tool_req["tool"],
        "payload": decision.payload,
    }


@router.post("/apply")
def apply_assistant_proposal_endpoint(
    body: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
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

    # Safety: proposal must match snapshot_id provided
    if proposal.snapshot_id != snapshot_id:
        raise HTTPException(409, "proposal_id does not match snapshot_id")

    snapshot = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot_id)
        .first()
    )
    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    new_snapshot = apply_assistant_proposal(
        db=db,
        user=user,
        snapshot=snapshot,
        station=proposal.station,
        tool_name=proposal.tool,
        payload=proposal.payload or {},
        confirm=confirm,
    )

    return {
        "new_snapshot_id": new_snapshot.id,
        "parent_snapshot_id": getattr(new_snapshot, "parent_snapshot_id", None),
        "status": "ok",
    }

