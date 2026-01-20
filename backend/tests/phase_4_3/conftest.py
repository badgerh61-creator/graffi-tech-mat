import pytest
from app.models.rendered_snapshot import SnapshotStatus


@pytest.fixture
def project_with_draft(
    db,
    project,
    completed_snapshot,
    editor_user,
):
    """
    Project that has an ACTIVE draft snapshot.
    Used to assert export blocking invariants.
    """

    # Ensure snapshot belongs to project
    completed_snapshot.project_id = project.id
    completed_snapshot.status = SnapshotStatus.COMPLETED.value
    db.commit()

    # Create draft snapshot
    draft = completed_snapshot.__class__(
        project_id=project.id,
        scene_state_hash=completed_snapshot.scene_state_hash,
        render_profile=completed_snapshot.render_profile,
        engine_version=completed_snapshot.engine_version,
        status=SnapshotStatus.DRAFT.value,
        parent_snapshot_id=completed_snapshot.id,
        created_by=editor_user.id,
    )

    db.add(draft)
    db.commit()

    return project

