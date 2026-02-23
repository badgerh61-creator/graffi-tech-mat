def test_execute_tool_invalid_tool_rejected_422(
    client,
    draft_snapshot,
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
            "snapshot_id": draft_snapshot.id,
            "station": geometry_station,
            "tool": "SHEAR",
            "payload": translate_request_payload,
        },
        headers=auth(editor_user),
    )

    assert r.status_code == 422
