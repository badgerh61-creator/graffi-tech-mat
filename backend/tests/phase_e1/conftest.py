# backend/tests/phase_e1/conftest.py
import pytest
from app.models.snapshot import Snapshot
from app.models.rendered_snapshot import SnapshotStatus


@pytest.fixture
def draft_snapshot_owned_by_other(db, draft_snapshot, viewer_user):
    draft_snapshot.owner_user_id = viewer_user.id
    db.commit()
    db.refresh(draft_snapshot)  # ✅ strict: ensure state is persisted + reloaded
    return draft_snapshot


@pytest.fixture
def blocked_execution_context():
    """
    Phase E.1 stub.
    Reason propagation is read-only in this phase.
    """
    return {
        "reason": "snapshot_locked_by_other_user"
    }

