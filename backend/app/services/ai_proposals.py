from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.audit import log_event
from app.models.rendered_snapshot import RenderedSnapshot


# =====================================================
# Phase R — Allowed AI interaction modes (AUTHORITATIVE)
# =====================================================

ALLOWED_MODES = {
    "analysis",
    "proposal",
    "review",
    "inquiry",  # 🔒 Phase R: read-only explanatory interaction
}


def request_ai_proposal(
    *,
    db: Session,
    user,
    snapshot: RenderedSnapshot,
    mode: str,
    prompt: str,
):
    """
    Phase R — AI proposal / interaction entrypoint.

    GUARANTEES:
    - No geometry mutation
    - No snapshot mutation
    - Fully audited
    """

    # ----------------------------
    # Permission enforcement
    # ----------------------------
    if user.role not in ("editor", "owner", "admin"):
        log_event(
            db,
            user_id=getattr(user, "id", None),
            action="ai.permission.denied",
            resource_type="snapshot",
            resource_id=snapshot.id,
            extra={"mode": mode},
        )
        raise HTTPException(403, "AI proposals require editor role")

    # ----------------------------
    # Mode validation
    # ----------------------------
    if mode not in ALLOWED_MODES:
        log_event(
            db,
            user_id=getattr(user, "id", None),
            action="ai.proposal.rejected",
            resource_type="snapshot",
            resource_id=snapshot.id,
            extra={"reason": "invalid_mode", "mode": mode},
        )
        raise HTTPException(422, "Invalid AI mode")

    # ----------------------------
    # Snapshot safety
    # ----------------------------
    if not snapshot.is_draft:
        raise HTTPException(409, "AI may only inspect draft snapshots")

    # ----------------------------
    # AUDIT (MANDATORY, MODE-SPECIFIC)
    # ----------------------------
    action = (
        "ai.interaction"
        if mode == "inquiry"
        else "ai.proposal.requested"
    )

    log_event(
        db,
        user_id=getattr(user, "id", None),
        action=action,
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={
            "mode": mode,
            "prompt": prompt,
        },
    )

    # ----------------------------
    # RETURN STRUCTURED RESPONSE
    # (NO MUTATION, EVER)
    # ----------------------------
    return {
        "mode": mode,
        "summary": "AI proposal request accepted",
        "proposals": [],   # 🔒 Phase R contract
        "mutations": [],
    }

