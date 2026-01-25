import pytest
from app.models.rendered_snapshot import RenderedSnapshot


@pytest.fixture
def solved_draft_snapshot(db, project, editor_user):
    """
    Phase K.1 test fixture.

    Phase K.1 expects curves to come from body_state["curves"].
    Phase J does NOT persist curves yet.
    Therefore tests inject them explicitly.
    """

    snapshot = RenderedSnapshot(
        project_id=project.id,

        # 🔒 REQUIRED identity
        scene_state_hash="test-scene-hash",
        render_profile="default",
        engine_version="test-engine",

        status="draft",
        body_state={
            "curves": [
                {
                    "id": "curve-a",
                    "parameters": {"length": 4.2},
                    "constraints": [],
                },
                {
                    "id": "curve-b",
                    "parameters": {"length": 4.2},
                    "constraints": [],
                },
            ]
        },
        created_by=editor_user.id,
    )

    db.add(snapshot)
    db.commit()

    return snapshot



