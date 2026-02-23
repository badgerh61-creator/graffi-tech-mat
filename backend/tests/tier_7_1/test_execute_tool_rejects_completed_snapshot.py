def test_execute_tool_rejects_completed_snapshot(
    client,
    completed_snapshot,
    editor_user,
    geometry_station,
    translate_request_payload,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.services.transform_tool_service._require_draft_lock_if_available",
        lambda **kwargs: None,
    )

    r = client.post(
        "/tools/execute",
        json={
            "snapshot_id": completed_snapshot.id,
            "station": geometry_station,
            "tool": "TRANSLATE",
            "payload": translate_request_payload,
        },
        headers=auth(editor_user),
    )

    assert r.status_code == 409
