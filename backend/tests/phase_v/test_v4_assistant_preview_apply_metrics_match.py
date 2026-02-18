from tests.phase_v.journey_helpers import force_db_lock, force_presence_session


def test_v4_assistant_preview_apply_metrics_match(
    client,
    db,
    owner_user,
    draft_snapshot,
    assistant_proposal_factory,
):
    """
    Current kernel (Phase T) does NOT allow station='tuning' (ALLOWED_STATIONS excludes it),
    so apply MUST be rejected by kernel with reason='station' — BUT ONLY if:

      - draft ownership is satisfied (require_draft_owner)
      - presence session is satisfied (require_active_session)
    """

    # ✅ satisfy draft ownership + lock
    force_db_lock(db, draft_snapshot, owner_user.id)

    # ✅ satisfy session authority
    force_presence_session(db, user=owner_user, snapshot=draft_snapshot)

    proposal = {
        "station": "tuning",  # invalid station per structural_guards.py
        "tool": "UPDATE_ENGINE_CONFIG",
        "payload": {"power_hp": 240, "torque_nm": 310},
    }

    # 1) Preview should succeed (preview path doesn't enforce Phase-T stations)
    r_prev = client.post(
        "/assistant/proposals/preview",
        json={"snapshot_id": draft_snapshot.id, "proposal": proposal},
        headers=auth(owner_user),
    )
    assert r_prev.status_code == 200

    prev = r_prev.json()
    assert "payload_hash" in prev
    assert "preview" in prev
    payload_hash = prev["payload_hash"]

    # 2) Persist proposal record
    p = assistant_proposal_factory(
        snapshot_id=draft_snapshot.id,
        station="tuning",
        tool="UPDATE_ENGINE_CONFIG",
        payload=proposal["payload"],
        created_by_user_id=owner_user.id,
    )

    # 3) Apply must now reach kernel and be rejected for station
    r_apply = client.post(
        "/assistant/proposals/apply",
        json={
            "proposal_id": p.id,
            "snapshot_id": draft_snapshot.id,
            "confirm": True,
            "payload_hash": payload_hash,
        },
        headers=auth(owner_user),
    )

    # helpful debugging if it ever regresses again
    if r_apply.status_code != 409:
        raise AssertionError(f"apply status={r_apply.status_code}\nbody={r_apply.text}\n")

    body = r_apply.json()
    assert "detail" in body
    assert "Kernel rejected proposal: station" in body["detail"]

