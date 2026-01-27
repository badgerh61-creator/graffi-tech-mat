import pytest
import uuid
from datetime import datetime

from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.models.user import User


# ---------------------------------------------
# Users
# ---------------------------------------------

@pytest.fixture
def user_a(db):
    user = User(
        email=f"user_a_{uuid.uuid4()}@test.com",
        hashed_password="x",
        role="viewer",
        is_active=True,
    )
    db.add(user)
    db.commit()
    return user


# ---------------------------------------------
# Second user (non-owner)
# ---------------------------------------------

@pytest.fixture
def user_b(db):
    user = User(
        email=f"user_b_{uuid.uuid4()}@test.com",
        hashed_password="x",
        role="viewer",
        is_active=True,
    )
    db.add(user)
    db.commit()
    return user


# ---------------------------------------------
# Draft snapshot owned by user A
# ---------------------------------------------

@pytest.fixture
def draft_snapshot_owned_by_user_a(db, project, user_a):
    snapshot = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="draft-hash",
        render_profile="default",
        engine_version="test",
        status=SnapshotStatus.DRAFT.value,
        created_by=user_a.id,
        owner_user_id=user_a.id,
        locked_at=datetime.utcnow(),
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot

