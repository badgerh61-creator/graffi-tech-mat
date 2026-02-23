def test_execute_translate_creates_child_draft_snapshot(
    client,
    db,
    draft_snapshot,
    editor_user,
    geometry_station,
    translate_request_payload,
    monkeypatch,
):
    # --- Allow Phase T evaluator ---
    class Allow:
        allowed = True
        reason = None

    monkeypatch.setattr(
        "app.services.studio_kernel_executor.evaluate_tool_invocation",
        lambda **kwargs: Allow(),
    )

    # --- Allow lock ---
    monkeypatch.setattr(
        "app.services.transform_tool_service._require_draft_lock_if_available",
        lambda **kwargs: None,
    )

    r = client.post(
        "/tools/execute",
        json={
            "snapshot_id": draft_snapshot.id,
            "station": geometry_station,
            "tool": "TRANSLATE",
            "payload": translate_request_payload,
        },
        headers=auth(editor_user),
    )

    assert r.status_code == 200

    new_id = r.json()["new_snapshot_id"]
    assert new_id != draft_snapshot.id

    new_snapshot = db.query(draft_snapshot.__class__).get(new_id)
    assert new_snapshot is not None
    assert new_snapshot.status == "draft"

    if hasattr(new_snapshot, "parent_snapshot_id"):
        assert new_snapshot.parent_snapshot_id == draft_snapshot.id
