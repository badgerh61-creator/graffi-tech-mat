import pytest
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus


@pytest.fixture
def constrained_draft_snapshot(db, project, editor_user):
    """
    Draft snapshot with curves + constraints.
    Used by Phase J.3 solver tests.
    """
    snapshot = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="hash-constrained",
        render_profile="default",
        engine_version="test-engine",
        status=SnapshotStatus.DRAFT.value,
        created_by=editor_user.id,
        body_state={
            "curves": [
                {
                    "id": "curve-1",
                    "type": "bezier",
                    # 🔒 Phase J.3 canonical key
                    "params": {
                        "length": 10,
                    },
                    "constraints": [
                        {
                            "type": "fixed_length",
                            "value": 10,
                        }
                    ],
                }
            ]
        },
    )

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot


@pytest.fixture
def unsatisfiable_constrained_snapshot(db, project, editor_user):
    """
    Draft snapshot whose constraints cannot be satisfied.
    """
    snapshot = RenderedSnapshot(
        project_id=project.id,
        scene_state_hash="hash-unsat",
        render_profile="default",
        engine_version="test-engine",
        status=SnapshotStatus.DRAFT.value,
        created_by=editor_user.id,
        body_state={
            "curves": [
                {
                    "id": "curve-1",
                    "type": "bezier",
                    # 🔒 Phase J.3 canonical key
                    "params": {
                        "length": 10,
                    },
                    "constraints": [
                        {
                            "type": "fixed_length",
                            "value": 9999,  # ❌ impossible → must fail
                        }
                    ],
                }
            ]
        },
    )

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot


@pytest.fixture
def conflicting_constraints_snapshot(unsatisfiable_constrained_snapshot):
    """
    Alias fixture — MUST behave identically.
    No special casing allowed.
    """
    return unsatisfiable_constrained_snapshot

