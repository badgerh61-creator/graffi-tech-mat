# backend/app/services/ai_assistant.py

from sqlalchemy.orm import Session
from app.services.ai_proposals import request_ai_proposal
from app.models.rendered_snapshot import RenderedSnapshot


class AssistantService:
    """
    Phase R — Adapter only.

    ZERO logic.
    ZERO mutation.
    Exists solely to satisfy the test contract.
    """

    def handle_request(
        self,
        *,
        db: Session,
        user,
        snapshot: RenderedSnapshot,
        mode: str,
        prompt: str,
    ):
        result = request_ai_proposal(
            db=db,
            user=user,
            snapshot=snapshot,
            mode=mode,
            prompt=prompt,
        )

        # 🔒 Phase R response-shape contract (additive only)
        result.setdefault("proposals", [])

        return result

