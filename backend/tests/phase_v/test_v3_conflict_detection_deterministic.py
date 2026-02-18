from tests.phase_v.journey_helpers import (
    force_db_lock,
    force_active_session,
    set_current_user,
    clear_current_user,
)


def test_v3_conflict_detection_deterministic(
    client,
    db,
    owner_user,
    draft_snapshot,
):
    """
    Determinism proof without mutations:
    - Create explicit SnapshotConflict row
    - Call /assistant/proposals/evaluate twice with same inputs
    - Expect identical outputs both times
    """
    from app.models.conflict import SnapshotConflict

    set_current_user(client, owner_user)

    force_db_lock(db, draft_snapshot, owner_user.id)
    force_active_session(
        db,
        user_id=owner_user.id,
        project_id=draft_snapshot.project_id,
        snapshot_id=draft_snapshot.id,
    )

    db.add(SnapshotConflict(snapshot_id=draft_snapshot.id, reason="explicit_conflict"))
    db.commit()

    body = {
        "snapshot_id": draft_snapshot.id,
        "proposal": {
            "station": "geometry",
            "tool": "translate",
            "payload": {"target_id": "panel-1", "x": 10},
        },
    }

    r1 = client.post("/assistant/proposals/evaluate", json=body)
    r2 = client.post("/assistant/proposals/evaluate", json=body)

    assert r1.status_code == 200, r1.text
    assert r2.status_code == 200, r2.text
    assert r1.json() == r2.json()

    clear_current_user(client)

