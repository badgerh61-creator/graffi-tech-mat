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
from app.services.assistant_proposal_applier import (
    apply_assistant_proposal,
    require_payload_hash_match,
)
from app.services.assistant_metrics_preview import preview_metrics_for_proposal

# ✅ MUST match tests: "/assistant/proposals/apply"
router = APIRouter(prefix="/assistant/proposals", tags=["assistant-proposals"])


def _load_snapshot_or_404(db: Session, snapshot_id: int) -> RenderedSnapshot:
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == int(snapshot_id))
        .first()
    )
    if not snapshot:
        raise HTTPException(404, "Snapshot not found")
    return snapshot


def _load_proposal_or_404(db: Session, proposal_id: str) -> AssistantProposal:
    # proposal_id is uuid-string in your model
    proposal = (
        db.query(AssistantProposal)
        .filter(AssistantProposal.id == str(proposal_id))
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
      B) { "snapshot_id": 123, "proposal_id": "uuid-string" }
    """
    snapshot_id = body.get("snapshot_id")
    if snapshot_id is None:
        raise HTTPException(422, "snapshot_id required")

    snapshot = _load_snapshot_or_404(db, int(snapshot_id))

    proposal_id = body.get("proposal_id")
    if proposal_id:
        p = _load_proposal_or_404(db, str(proposal_id))
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
            "proposal_id": str(proposal_id) if proposal_id else None,
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


@router.post("/preview")
def preview_assistant_proposal(
    body: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Tier 4.6 — Deterministic metrics preview + diff.

    Input:
      {
        "snapshot_id": 123,
        "proposal": { "station": "tuning", "tool": "...", "payload": {...} }
      }
    """
    snapshot_id = body.get("snapshot_id")
    proposal = body.get("proposal") or {}

    if snapshot_id is None:
        raise HTTPException(422, "snapshot_id required")

    snapshot = _load_snapshot_or_404(db, int(snapshot_id))

    tool = proposal.get("tool")
    payload = proposal.get("payload") or {}

    if not tool or not isinstance(tool, str):
        raise HTTPException(422, "proposal.tool required")
    if not isinstance(payload, dict):
        raise HTTPException(422, "proposal.payload must be an object")

    vehicle_constants = {
        "mass_kg": getattr(snapshot, "vehicle_mass_kg", None),
    }

    result = preview_metrics_for_proposal(
        snapshot_id=snapshot.id,
        tool=tool,
        payload=payload,
        tuning_state=getattr(snapshot, "tuning_state", None) or {},
        vehicle_constants=vehicle_constants,
    )

    log_event(
        db=db,
        user_id=getattr(user, "id", None),
        action="assistant.proposal.previewed",
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={
            "tool": tool,
            "payload_hash": result.get("payload_hash"),
        },
    )

    return result


@router.post("/apply")
def apply_assistant_proposal_endpoint(
    body: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Tier 4.5 apply endpoint (Tier 4.6-compatible):

    - confirm=true required (Tier 4.5 invariant)
    - payload_hash enforcement:
        * optional for backward compatibility with Tier 4.5 tests
        * if provided => MUST match (Tier 4.6 invariant)
    """
    proposal_id = body.get("proposal_id")
    snapshot_id = body.get("snapshot_id")
    confirm = body.get("confirm", False)
    payload_hash = body.get("payload_hash")  # optional

    if not proposal_id:
        raise HTTPException(422, "proposal_id required")
    if snapshot_id is None:
        raise HTTPException(422, "snapshot_id required")

    proposal = _load_proposal_or_404(db, str(proposal_id))

    if int(proposal.snapshot_id) != int(snapshot_id):
        raise HTTPException(409, "proposal_id does not match snapshot_id")

    snapshot = _load_snapshot_or_404(db, int(snapshot_id))

    # ✅ Tier 4.6 enforcement only if caller supplies hash
    if payload_hash is not None:
        require_payload_hash_match(
            db=db,
            proposal_id=str(proposal_id),
            snapshot_id=int(snapshot_id),
            payload_hash=str(payload_hash),
        )

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

