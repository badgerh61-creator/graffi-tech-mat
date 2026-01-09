import pytest
from app.models.rendered_snapshot import RenderedSnapshot


@pytest.fixture
def completed_snapshot_with_decal(db, project, admin_user):
    """
    Phase K.1 fixture:
    A completed snapshot with a synthetic decor state attached
    for mutation testing.

    NOTE:
    - RenderedSnapshot does NOT persist decor yet
    - Decor state is attached dynamically for Phase K tests
    """
    snapshot = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="__decor_with_decal__",
        render_profile="default",
        engine_version="test-engine",
        status="completed",
        created_by=admin_user.id,
    )

    # 👇 Attach decor state dynamically (test-only)
    snapshot.decor_state = {
        "decals": [
            {
                "instance_id": "abc123",
                "panel": "door_left",
                "uv": {
                    "x": 0.2,
                    "y": 0.2,
                    "scale": 1.0,
                    "rotation": 0,
                },
            }
        ]
    }

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot

