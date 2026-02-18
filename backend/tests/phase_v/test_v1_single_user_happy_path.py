from tests.phase_v.journey_helpers import (
    force_db_lock,
    force_active_session,
    set_current_user,
    clear_current_user,
)


def test_v1_single_user_happy_path(
    client,
    db,
    owner_user,
    draft_snapshot,
    assistant_proposal_factory,
):
    set_current_user(client, owner_user)

    # 1) Lock + active session
    force_db_lock(db, draft_snapshot, owner_user.id)
    force_active_session(
        db,
        user_id=owner_user.id,
        project_id=draft_snapshot.project_id,
        snapshot_id=draft_snapshot.id,
    )

    # 2) Apply tool via assistant apply
    p = assistant_proposal_factory(
        snapshot_id=draft_snapshot.id,
        station="geometry",
        tool="translate",
        payload={"target_id": "panel-1", "x": 10},
        created_by_user_id=owner_user.id,
    )

    r_apply = client.post(
        "/assistant/proposals/apply",
        json={"proposal_id": p.id, "snapshot_id": draft_snapshot.id, "confirm": True},
    )
    assert r_apply.status_code == 200, r_apply.text
    new_snapshot_id = r_apply.json()["new_snapshot_id"]

    # 3) Finalize (your real route is /snapshots/{id}/finalize)
    r_fin = client.post(f"/snapshots/{new_snapshot_id}/finalize")
    assert r_fin.status_code == 200, r_fin.text
    completed_id = r_fin.json().get("snapshot_id") or new_snapshot_id

    # 4) Completed snapshot immutable
    p2 = assistant_proposal_factory(
        snapshot_id=completed_id,
        station="geometry",
        tool="translate",
        payload={"target_id": "panel-1", "x": 5},
        created_by_user_id=owner_user.id,
    )
    r_apply2 = client.post(
        "/assistant/proposals/apply",
        json={"proposal_id": p2.id, "snapshot_id": completed_id, "confirm": True},
    )
    assert r_apply2.status_code == 409, r_apply2.text

    clear_current_user(client)

