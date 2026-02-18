from tests.phase_v.journey_helpers import (
    force_db_lock,
    force_active_session,
    set_current_user,
    clear_current_user,
)


def test_v5_tool_flow_mode_enforcement(
    client,
    db,
    owner_user,
    draft_snapshot,
    assistant_proposal_factory,
):
    set_current_user(client, owner_user)

    force_db_lock(db, draft_snapshot, owner_user.id)
    force_active_session(
        db,
        user_id=owner_user.id,
        project_id=draft_snapshot.project_id,
        snapshot_id=draft_snapshot.id,
    )

    p = assistant_proposal_factory(
        snapshot_id=draft_snapshot.id,
        station="review",  # wrong station
        tool="translate",
        payload={"target_id": "panel-1", "x": 1},
        created_by_user_id=owner_user.id,
    )

    r = client.post(
        "/assistant/proposals/apply",
        json={"proposal_id": p.id, "snapshot_id": draft_snapshot.id, "confirm": True},
    )
    assert r.status_code in (403, 409, 422), r.text

    clear_current_user(client)

