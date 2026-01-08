from sqlalchemy.orm import Session
from typing import Dict, Any

from app.models.mutation_journal import MutationJournal


def write_journal_entry(
    *,
    db: Session,
    intent_type: str,
    target_type: str,
    target_id: int,
    before_state: Dict[str, Any],
    after_state: Dict[str, Any],
    issued_by_user_id: int,
    reason: str | None = None,
) -> MutationJournal:
    """
    Canonical journal writer (Phase I + Phase K compliant)
    """

    entry = MutationJournal(
        intent_type=intent_type,
        target_type=target_type,
        target_id=target_id,
        before_state=before_state,
        after_state=after_state,
        issued_by_user_id=issued_by_user_id,
        reason=reason,
    )

    db.add(entry)
    db.flush()

    return entry

