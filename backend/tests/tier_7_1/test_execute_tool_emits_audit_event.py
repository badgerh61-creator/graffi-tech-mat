def test_execute_tool_emits_audit_event(
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

    from app.models.audit_log import AuditLog  # adjust if needed

    events = (
        db.query(AuditLog)
        .filter(AuditLog.action == "snapshot.transform")
        .filter(AuditLog.resource_id == new_id)
        .all()
    )

    assert len(events) == 1
