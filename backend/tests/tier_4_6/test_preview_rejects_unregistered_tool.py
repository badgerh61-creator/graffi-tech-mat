def test_preview_rejects_unregistered_tool(
    client,
    draft_snapshot_with_tuning,
    viewer_user,
):
    body = {
        "snapshot_id": draft_snapshot_with_tuning.id,
        "proposal": {
            "station": "tuning",
            "tool": "NOT_A_REAL_TOOL",
            "payload": {"x": 1},
        },
    }

    r = client.post("/assistant/proposals/preview", json=body, headers=auth(viewer_user))
    assert r.status_code == 422

