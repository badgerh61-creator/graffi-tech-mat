import pytest
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus


# =====================================================
# Phase 5.5 — Snapshot Graph Fixtures
# =====================================================

@pytest.fixture
def root_snapshot(db, project, editor_user):
    """
    A snapshot with NO parent.
    Used to assert undo is blocked at root.
    """
    snap = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="root",
        render_profile="default",
        engine_version="test-engine",
        status=SnapshotStatus.DRAFT.value,
        created_by=editor_user.id,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


@pytest.fixture
def transformed_snapshot(db, root_snapshot, editor_user):
    """
    A snapshot WITH a parent.
    Used for undo/redo traversal.
    """
    child = root_snapshot.clone_for_mutation(
        created_by=editor_user.id
    )
    db.add(child)
    db.commit()
    db.refresh(child)
    return child


@pytest.fixture
def root_snapshot_with_child(root_snapshot, transformed_snapshot):
    """
    Alias fixture used by redo tests.
    """
    return root_snapshot


@pytest.fixture
def latest_snapshot(transformed_snapshot):
    """
    Alias for leaf snapshot in chain.
    """
    return transformed_snapshot

