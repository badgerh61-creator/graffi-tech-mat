from tests.phase_v.journey_helpers import (
    force_db_lock,
    force_active_session,
    set_current_user,
    clear_current_user,
)


def test_v2_lock_contention_and_handoff(
    client,
    db,
    owner_user,
    non_owner_user,
    draft_snapshot,
    assistant_proposal_factory,
):
    user_a = owner_user
    user_b = non_owner_user

    # A locks + sessions for both
    force_db_lock(db, draft_snapshot, user_a.id)
    force_active_session(db, user_id=user_a.id, project_id=draft_snapshot.project_id, snapshot_id=draft_snapshot.id)
    force_active_session(db, user_id=user_b.id, project_id=draft_snapshot.project_id, snapshot_id=draft_snapshot.id)

    # B tries apply -> blocked
    set_current_user(client, user_b)
    p_b = assistant_proposal_factory(
        snapshot_id=draft_snapshot.id,
        station="geometry",
        tool="translate",
        payload={"target_id": "panel-1", "x": 1},
        created_by_user_id=user_b.id,
    )
    r_apply_b = client.post(
        "/assistant/proposals/apply",
        json={"proposal_id": p_b.id, "snapshot_id": draft_snapshot.id, "confirm": True},
    )
    assert r_apply_b.status_code in (403, 409), r_apply_b.text

    # Handoff (no endpoint mounted) -> transfer owner in DB
    draft_snapshot.owner_user_id = user_b.id
    db.add(draft_snapshot)
    db.commit()

    # B applies successfully
    p_b2 = assistant_proposal_factory(
        snapshot_id=draft_snapshot.id,
        station="geometry",
        tool="translate",
        payload={"target_id": "panel-1", "x": 2},
        created_by_user_id=user_b.id,
    )
    r_apply_b2 = client.post(
        "/assistant/proposals/apply",
        json={"proposal_id": p_b2.id, "snapshot_id": draft_snapshot.id, "confirm": True},
    )
    assert r_apply_b2.status_code == 200, r_apply_b2.text

    clear_current_user(client)

