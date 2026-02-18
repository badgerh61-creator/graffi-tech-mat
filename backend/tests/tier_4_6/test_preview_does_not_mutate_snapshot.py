def test_preview_does_not_mutate_snapshot(
    db,
    client,
    draft_snapshot_with_tuning,
    viewer_user,
):
    before = dict(draft_snapshot_with_tuning.tuning_state or {})

    body = {
        "snapshot_id": draft_snapshot_with_tuning.id,
        "proposal": {
            "station": "tuning",
            "tool": "UPDATE_ENGINE_CONFIG",
            "payload": {"power_hp": 260},
        },
    }

    r = client.post("/assistant/proposals/preview", json=body, headers=auth(viewer_user))
    assert r.status_code == 200

    db.refresh(draft_snapshot_with_tuning)
    after = dict(draft_snapshot_with_tuning.tuning_state or {})

    assert after == before

