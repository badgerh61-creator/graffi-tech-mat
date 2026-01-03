from typing import Optional
from sqlalchemy.orm import Session

from app.models.mutation_journal import MutationJournal


class JournalResolutionResult:
    def __init__(
        self,
        *,
        journal: Optional[MutationJournal],
        new_cursor_id: Optional[int],
        noop: bool = False,
    ):
        self.journal = journal
        self.new_cursor_id = new_cursor_id
        self.noop = noop


class JournalResolver:
    @staticmethod
    def resolve(
        *,
        db: Session,
        model_id: int,
        cursor_id: int,
        direction: str,
    ) -> JournalResolutionResult:

        if direction not in ("undo", "redo"):
            raise ValueError("Invalid replay direction")

        # Fetch all journal IDs for this model in order
        journal_ids = (
            db.query(MutationJournal.id)
            .filter(
                MutationJournal.target_type == "model",
                MutationJournal.target_id == model_id,
            )
            .order_by(MutationJournal.id.asc())
            .all()
        )

        ids = [row.id for row in journal_ids]

        if not ids:
            return JournalResolutionResult(
                journal=None,
                new_cursor_id=cursor_id,
                noop=True,
            )

        # ----- UNDO -----
        if direction == "undo":
            if cursor_id not in ids:
                raise ValueError("Cursor journal not found")

            index = ids.index(cursor_id)

            # At beginning → no-op
            if index == 0:
                return JournalResolutionResult(
                    journal=None,
                    new_cursor_id=cursor_id,
                    noop=True,
                )

            journal = (
                db.query(MutationJournal)
                .filter(MutationJournal.id == cursor_id)
                .first()
            )

            return JournalResolutionResult(
                journal=journal,
                new_cursor_id=ids[index - 1],
                noop=False,
            )

        # ----- REDO -----
        if direction == "redo":
            if cursor_id not in ids:
                raise ValueError("Cursor journal not found")

            index = ids.index(cursor_id)

            # At end → no-op
            if index == len(ids) - 1:
                return JournalResolutionResult(
                    journal=None,
                    new_cursor_id=cursor_id,
                    noop=True,
                )

            next_journal_id = ids[index + 1]
            journal = (
                db.query(MutationJournal)
                .filter(MutationJournal.id == next_journal_id)
                .first()
            )

            return JournalResolutionResult(
                journal=journal,
                new_cursor_id=next_journal_id,
                noop=False,
            )

