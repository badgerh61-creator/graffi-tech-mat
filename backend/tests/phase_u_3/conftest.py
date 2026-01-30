import pytest
from datetime import datetime

from app.models.snapshot import Snapshot
from app.models.rendered_snapshot import RenderedSnapshot

@pytest.fixture
def stale_draft_snapshot(
    db,
    completed_snapshot,
    editor_user,
):
    """
    Draft snapshot whose parent is no longer the latest snapshot.
    Uses existing completed snapshot to preserve DB invariants.
    """

    # 1️⃣ Create a NEW completed snapshot (this becomes latest)
    newer_completed = Snapshot(
        project_id=completed_snapshot.project_id,
        parent_snapshot_id=completed_snapshot.id,
        scene_state_hash="__newer_completed__",
        status="completed",

        # 🔒 REQUIRED FIELDS (copied, not guessed)
        render_profile=completed_snapshot.render_profile,
        engine_version=completed_snapshot.engine_version,
        deterministic_key=completed_snapshot.deterministic_key,

        created_by=editor_user.id,
        owner_user_id=editor_user.id,
        created_at=datetime.utcnow(),
    )
    db.add(newer_completed)
    db.commit()
    db.refresh(newer_completed)

    # 2️⃣ Create a draft that still points to the OLD parent
    stale_draft = Snapshot(
        project_id=completed_snapshot.project_id,
        parent_snapshot_id=completed_snapshot.id,  # ❌ stale
        scene_state_hash="__stale_draft__",
        status="draft",

        # 🔒 REQUIRED FIELDS
        render_profile=completed_snapshot.render_profile,
        engine_version=completed_snapshot.engine_version,
        deterministic_key=completed_snapshot.deterministic_key,

        created_by=editor_user.id,
        owner_user_id=editor_user.id,
        created_at=datetime.utcnow(),
    )
    db.add(stale_draft)
    db.commit()
    db.refresh(stale_draft)

    return stale_draft


@pytest.fixture
def conflicted_draft_snapshot(db, stale_draft_snapshot):
    stale_draft_snapshot.is_conflicted = True
    stale_draft_snapshot.conflict_reason = "stale_parent"
    db.commit()
    return stale_draft_snapshot


@pytest.fixture
def latest_snapshot(db, completed_snapshot):
    """
    Phase U.3 semantic alias.

    latest_snapshot == most recent completed snapshot
    """
    return (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == completed_snapshot.project_id,
            RenderedSnapshot.status == "completed",
        )
        .order_by(RenderedSnapshot.created_at.desc())
        .first()
    )

