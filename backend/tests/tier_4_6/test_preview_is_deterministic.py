def test_preview_is_deterministic(
    client,
    draft_snapshot_with_tuning,
    viewer_user,
):
    body = {
        "snapshot_id": draft_snapshot_with_tuning.id,
        "proposal": {
            "station": "tuning",
            "tool": "UPDATE_ENGINE_CONFIG",
            "payload": {"power_hp": 220},
        },
    }

    r1 = client.post("/assistant/proposals/preview", json=body, headers=auth(viewer_user))
    r2 = client.post("/assistant/proposals/preview", json=body, headers=auth(viewer_user))

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json() == r2.json()

