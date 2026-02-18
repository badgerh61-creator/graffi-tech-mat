# backend/tests/tier_4_6/conftest.py

import pytest

from app.models.assistant_proposal import AssistantProposal
from app.services.draft_lock_service import acquire_draft_lock


@pytest.fixture
def draft_snapshot_with_tuning(db, draft_snapshot):
    """
    Ensure tuning_state exists and is committed, so preview is deterministic.
    """
    if getattr(draft_snapshot, "tuning_state", None) is None:
        draft_snapshot.tuning_state = {"engine": {"power_hp": 160, "torque_nm": 220}}
        db.add(draft_snapshot)
        db.commit()
        db.refresh(draft_snapshot)
    return draft_snapshot


@pytest.fixture
def locked_owner_user(db, owner_user, draft_snapshot_with_tuning):
    """
    Acquire the canonical U.2 draft lock for this user + snapshot.
    """
    acquire_draft_lock(db=db, snapshot=draft_snapshot_with_tuning, user=owner_user)
    return owner_user


@pytest.fixture
def assistant_proposal(db, owner_user, draft_snapshot_with_tuning):
    """
    IMPORTANT:
    - Do NOT set id to UUID string.
    - Let DB assign integer PK.
    """
    p = AssistantProposal(
        snapshot_id=int(draft_snapshot_with_tuning.id),
        station="tuning",
        tool="UPDATE_ENGINE_CONFIG",
        payload={"boost": 1.2},
        rationale="test proposal",
        risk_level="low",
        created_by_user_id=int(owner_user.id),
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

