def test_preview_returns_baseline_preview_diff_and_hash(
    client,
    draft_snapshot_with_tuning,
    viewer_user,
):
    body = {
        "snapshot_id": draft_snapshot_with_tuning.id,
        "proposal": {
            "station": "tuning",
            "tool": "UPDATE_ENGINE_CONFIG",
            "payload": {"power_hp": 240, "torque_nm": 310},
        },
    }

    r = client.post(
        "/assistant/proposals/preview",
        json=body,
        headers=auth(viewer_user),
    )

    assert r.status_code == 200
    data = r.json()

    assert "baseline" in data
    assert "preview" in data
    assert "diff" in data
    assert "risk_notes" in data
    assert "payload_hash" in data

    assert isinstance(data["risk_notes"], list)
    assert isinstance(data["payload_hash"], str)
    assert len(data["payload_hash"]) >= 32

