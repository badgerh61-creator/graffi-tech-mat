from sqlalchemy.orm import Session
from typing import Dict, Any

from app.models.journal_entry import JournalEntry
from app.models.mutation_journal import MutationJournal


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
):
    """
    Canonical journal writer (Phase I + Phase K compliant)

    NOTE:
    Phase K requires dual-write:
    - journal_entries (canonical)
    - mutation_journal (legacy audit surface)
    """

    db.flush()

    # -----------------------------------------------------
    # ✅ Canonical journal entry
    # -----------------------------------------------------
    canonical = JournalEntry(
        type="mutation",
        scene_id=None,
        snapshot_id=after_state["snapshot_id"],
        actor_user_id=issued_by_user_id,
        scene_hash=None,

        project_id=project_id,
        actor_id=issued_by_user_id,
        mutation_type=intent_type,
        snapshot_before=before_state["snapshot_id"],
        snapshot_after=after_state["snapshot_id"],
    )
    db.add(canonical)

    # -----------------------------------------------------
    # ✅ Legacy mutation journal entry (Phase K tests rely on this)
    # -----------------------------------------------------
    legacy = MutationJournal(
        intent_type=intent_type,
        target_type=target_type,
        target_id=target_id,
        before_state=before_state,
        after_state=after_state,
        issued_by_user_id=issued_by_user_id,
        reason=reason,
    )
    db.add(legacy)

    db.flush()

    return canonical

