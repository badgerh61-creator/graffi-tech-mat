import pytest
from datetime import datetime, timezone

from app.models.job import Job
from app.models.mutation_journal import MutationJournal


def _auto_value_for_column(col, *, admin_user=None, draft_snapshot=None, project=None):
    """
    Best-effort deterministic filler for NOT NULL columns.
    - Uses existing fixtures when column looks like a foreign key
    - Otherwise fills by type
    """
    name = col.name.lower()

    # Common FK-ish names
    if admin_user is not None and ("user_id" in name or name in ("actor_id", "created_by", "created_by_user_id")):
        return admin_user.id
    if draft_snapshot is not None and ("snapshot_id" in name or "rendered_snapshot_id" in name):
        return draft_snapshot.id
    if project is not None and ("project_id" in name):
        return project.id

    # Fill by python type
    try:
        pytype = col.type.python_type
    except Exception:
        pytype = None

    if pytype is int:
        return 1
    if pytype is str:
        # intent_type was your failing NOT NULL earlier
        if "intent" in name and "type" in name:
            return "TEST_INTENT"
        return "test"
    if pytype is bool:
        return False
    if pytype is float:
        return 0.0
    if "datetime" in str(col.type).lower() or pytype is datetime:
        return datetime.now(timezone.utc)

    # JSON-ish / unknown types
    return {}


@pytest.fixture
def mutation_journal_entry(db, admin_user, draft_snapshot, project):
    """
    Phase H.3 needs a real MutationJournal row because Job.mutation_id is NOT NULL + FK.
    We build a row that satisfies all NOT NULL columns without guessing your full schema.
    """
    mj = MutationJournal()

    # Fill required cols (NOT NULL, no default, not PK)
    for col in MutationJournal.__table__.columns:
        if col.primary_key:
            continue
        if col.nullable:
            continue
        if col.default is not None or col.server_default is not None:
            continue

        # Skip if already set by constructor
        if getattr(mj, col.name, None) is not None:
            continue

        setattr(
            mj,
            col.name,
            _auto_value_for_column(
                col,
                admin_user=admin_user,
                draft_snapshot=draft_snapshot,
                project=project,
            ),
        )

    db.add(mj)
    db.commit()
    db.refresh(mj)
    return mj


@pytest.fixture
def job_factory(db, mutation_journal_entry):
    def _make(
        *,
        status: str = "QUEUED",
        attempts: int = 0,
        max_attempts: int = 3,
        next_run_at=None,
        started_at=None,
        idempotency_key=None,
        job_type: str = "test_job",
        target_type: str = "system",
        target_id: int = 1,
        mutation_id: int | None = None,
    ) -> Job:
        j = Job(
            mutation_id=mutation_id or mutation_journal_entry.id,
            job_type=job_type,
            target_type=target_type,
            target_id=target_id,
            idempotency_key=idempotency_key,
            next_run_at=next_run_at,
            started_at=started_at,
        )
        j.status = status
        j.attempts = attempts
        j.max_attempts = max_attempts

        db.add(j)
        db.commit()
        db.refresh(j)
        return j

    return _make

