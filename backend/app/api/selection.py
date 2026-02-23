from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.services.selection_resolution import resolve_selection

router = APIRouter(prefix="/selection", tags=["selection"])


@router.post("/resolve")
def resolve_selection_endpoint(
    body: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Tier 7.6 helper endpoint (optional but testable).
    Read-only: resolves selection deterministically.
    """
    hit_candidates = body.get("hit_candidates")
    modifiers = body.get("modifiers") or {}
    previous_selection = body.get("previous_selection") or {}

    state = resolve_selection(
        hit_candidates=hit_candidates,
        modifiers=modifiers,
        previous_selection=previous_selection,
    )
    return {
        "selected_target_ids": state.selected_target_ids,
        "active_target_id": state.active_target_id,
        "winner": state.winner,
    }
