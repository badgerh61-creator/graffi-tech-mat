import pytest
from datetime import datetime, timedelta

from app.models.snapshot import Snapshot
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.models.job import Job
from app.models.mutation_journal import MutationJournal

@pytest.fixture
def expired_draft_snapshot(db, project, editor_user):
    snapshot = Snapshot(
        project_id=project.id,              # ✅ real project
        status="draft",
        scene_state_hash="__draft__",
        engine_version="test-engine",
        render_profile="default",
        created_by=editor_user.id,           # ✅ real user
        created_at=datetime.utcnow() - timedelta(days=2),
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot

@pytest.fixture
def abandoned_snapshot(db, project, editor_user):
    snapshot = RenderedSnapshot(
        project_id=project.id,
        status=SnapshotStatus.ABANDONED.value,
        scene_state_hash="__abandoned__",
        render_profile="default",
        engine_version="test-engine",
        created_by=editor_user.id,
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot

@pytest.fixture
def mutation_journal(db, editor_user):
    mj = MutationJournal(
        intent_type="system.retry",
        target_type="job",
        target_id=1,
        before_state={},
        after_state={},
        issued_by_user_id=editor_user.id,
        reason="test",
    )
    db.add(mj)
    db.commit()
    db.refresh(mj)
    return mj

@pytest.fixture
def failing_job(db, mutation_journal):
    job = Job(
        mutation_id=mutation_journal.id,
        job_type="test",
        target_type="snapshot",
        target_id=1,
        state="RUNNING",
        retry_count=3,
        max_retries=3,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

class FakeQueue:
    def __init__(self, depth):
        self.depth = depth


@pytest.fixture
def saturated_queue():
    return FakeQueue(depth=1000)

@pytest.fixture
def orphaned_job(db, mutation_journal):
    job = Job(
        mutation_id=mutation_journal.id,
        job_type="startup",
        target_type="system",
        target_id=0,
        state="RUNNING",   # 👈 critical
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@pytest.fixture
def corrupted_snapshot(db, project, editor_user):
    snapshot = Snapshot(
        project_id=project.id,
        status="draft",
        is_corrupted=True,
        scene_state_hash="__corrupt__",
        engine_version="test-engine",
        render_profile="default",
        created_by=editor_user.id,
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot

