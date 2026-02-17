# backend/tests/tier_4_5/conftest.py
import pytest

from app.models.rendered_snapshot import RenderedSnapshot
from app.models.assistant_proposal import AssistantProposal
from app.services.draft_lock_service import acquire_draft_lock, get_draft_lock

# ✅ ADD THIS (canonical for require_active_session)
from app.services.presence_sessions import start_session


@pytest.fixture
def locked_owner_user(db, owner_user, assistant_proposal):
    db.flush()

    snap = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == assistant_proposal.snapshot_id)
        .first()
    )
    assert snap is not None, "assistant_proposal.snapshot_id must reference a real RenderedSnapshot"

    acquire_draft_lock(db=db, snapshot=snap, user=owner_user)

    lock = get_draft_lock(db=db, snapshot=snap)
    assert lock is not None, "Lock was not created"
    assert lock.user_id == owner_user.id, f"Lock owner mismatch: {lock.user_id} != {owner_user.id}"

    # ✅ NEW: establish active presence session (unblocks “No active session”)
    start_session(db=db, user=owner_user, project_id=snap.project_id)

    return owner_user


@pytest.fixture
def editor_user_without_lock(editor_user):
    return editor_user


@pytest.fixture
def assistant_proposal(db, draft_snapshot, owner_user):
    """
    Proposal stored in DB (Tier 4.5 canonical input uses proposal_id).
    """
    p = AssistantProposal(
        snapshot_id=draft_snapshot.id,
        station="geometry",
        tool="translate",
        payload={"target_id": "panel-1", "x": 10},
        risk_level="low",
        created_by_user_id=owner_user.id,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@pytest.fixture
def unregistered_tool_proposal(db, draft_snapshot, owner_user):
    """
    Used by test_apply_proposal_rejects_tool_not_registered.py
    """
    p = AssistantProposal(
        snapshot_id=draft_snapshot.id,
        station="geometry",
        tool="NOT_A_REAL_TOOL",
        payload={"target_id": "panel-1", "x": 10},
        risk_level="low",
        created_by_user_id=owner_user.id,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

