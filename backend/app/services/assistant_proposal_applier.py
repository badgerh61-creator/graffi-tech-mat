# backend/app/services/assistant_proposal_applier.py
from __future__ import annotations

from typing import Any, Dict

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.audit import log_event
from app.services.tool_registry import get_tool
from app.services.studio_kernel_executor import evaluate_tool_invocation
from app.services.draft_lock_service import require_draft_owner  # ✅ canonical in your tree

from app.crud.assistant_proposals import get_proposal
from app.services.proposal_hashing import compute_payload_hash


_TRANSFORM_OPS = {"translate", "rotate", "scale"}


def require_payload_hash_match(
    *,
    db: Session,
    proposal_id: str,
    snapshot_id: int,
    payload_hash: str,
):
    """
    Tier 4.6 — Apply-time payload hash enforcement.

    Ensures the proposal payload being applied is exactly what was previewed.
    """
    proposal = get_proposal(db, proposal_id)
    if not proposal:
        raise HTTPException(404, "Proposal not found")

    if int(proposal.snapshot_id) != int(snapshot_id):
        raise HTTPException(409, "Proposal snapshot mismatch")

    expected = compute_payload_hash(
        snapshot_id=int(proposal.snapshot_id),
        tool=str(proposal.tool),
        payload=proposal.payload or {},
    )

    if str(payload_hash) != expected:
        raise HTTPException(409, "Proposal payload hash mismatch")

    return proposal


def _kernel_tool_for(tool_name: str) -> str:
    # Phase T kernel tools are categories, not leaf operations
    if tool_name in _TRANSFORM_OPS:
        return "transform"
    return tool_name


def apply_assistant_proposal(
    *,
    db: Session,
    user,
    snapshot,
    station: str,
    tool_name: str,
    payload: Dict[str, Any],
    confirm: bool,
):
    """
    Tier 4.5 — executes a proposal ONLY through:
    - confirm gate
    - draft-only gate
    - U.2 lock enforcement
    - tool registry enforcement
    - Phase T kernel evaluation
    - audited execution

    Tier 4.6 hash enforcement happens before this is called (API layer),
    to avoid changing Tier 4.5 semantics.
    """
    if confirm is not True:
        raise HTTPException(409, "confirm=true required")

    if getattr(snapshot, "status", None) != "draft":
        raise HTTPException(409, "Snapshot must be draft")

    # ✅ U.2 ownership/locking enforcement (canonical)
    snapshot = require_draft_owner(db=db, snapshot=snapshot, user=user)

    # ✅ Tool registry enforcement FIRST (tests expect 422 if unknown)
    tool = get_tool(tool_name)  # raises HTTPException(422, ...) if unknown

    # ✅ Kernel tool category mapping (translate/rotate/scale => transform)
    kernel_tool = _kernel_tool_for(tool_name)

    # ✅ Phase T kernel evaluation (authoritative)
    decision = evaluate_tool_invocation(
        user=user,
        snapshot=snapshot,
        station=station,
        tool=kernel_tool,
        payload=payload,
    )
    if not decision.allowed:
        raise HTTPException(409, f"Kernel rejected proposal: {decision.reason}")

    # Execute leaf tool (registry controls actual executor)
    new_snapshot = tool.execute(
        db=db,
        snapshot=snapshot,
        user=user,
        params=payload,
    )

    log_event(
        db,
        user_id=getattr(user, "id", None),
        action="assistant.proposal.applied",
        resource_type="snapshot",
        resource_id=getattr(new_snapshot, "id", None),
        extra={
            "from_snapshot_id": getattr(snapshot, "id", None),
            "station": station,
            "kernel_tool": kernel_tool,
            "tool": tool_name,
            "confirm": True,
        },
    )

    return new_snapshot

