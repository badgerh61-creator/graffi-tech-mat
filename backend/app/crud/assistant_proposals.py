from sqlalchemy.orm import Session
from app.models.assistant_proposal import AssistantProposal


def get_proposal(db: Session, proposal_id: str) -> AssistantProposal | None:
    return db.query(AssistantProposal).get(proposal_id)

