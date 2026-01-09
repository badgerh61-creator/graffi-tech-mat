from sqlalchemy.orm import Session
from typing import Dict, Any

from app.models.journal_entry import JournalEntry


def write_journal_entry(
    *,
    db: Session,
    project_id: int,
    intent_type: str,
    target_type: str,
    target_id: int,
    before_state: Dict[str, Any],
    after_state: Dict[str, Any],
    issued_by_user_id: int,
    reason: str | None = None,
) -> JournalEntry:
    """
    Canonical journal writer (Phase I + Phase K compliant)
    """

    # Ensure FK targets exist
    db.flush()

    entry = JournalEntry(
        # -----------------------------------------------------
        # Legacy-required fields (schema compatibility)
        # -----------------------------------------------------
        type="mutation",
        scene_id=None,
        snapshot_id=after_state["snapshot_id"],
        actor_user_id=issued_by_user_id,
        scene_hash=None,

        # -----------------------------------------------------
        # Canonical fields
        # -----------------------------------------------------
        project_id=project_id,
        actor_id=issued_by_user_id,
        mutation_type=intent_type,
        snapshot_before=before_state["snapshot_id"],
        snapshot_after=after_state["snapshot_id"],
    )

    db.add(entry)
    db.flush()

    return entry

