def test_execute_tool_audit_includes_snap_metadata(
    client,
    db,
    draft_snapshot,
    editor_user,
    monkeypatch,
):
    # Phase U lock passes
    monkeypatch.setattr(
        "app.services.transform_tool_service._require_draft_lock_if_available",
        lambda **kwargs: None,
    )

    # Phase T kernel gate allows
    class Allow:
        allowed = True
        reason = None

    monkeypatch.setattr(
        "app.services.studio_kernel_executor.evaluate_tool_invocation",
        lambda **kwargs: Allow(),
    )

    # IMPORTANT:
    # Your schema only preserves payload.target_id + payload.params.
    # So Tier 7.3 snap fields must be inside params.
    r = client.post(
        "/tools/execute",
        json={
            "snapshot_id": draft_snapshot.id,
            "station": "geometry",
            "tool": "TRANSLATE",
            "payload": {
                "target_id": "panel-1",
                "params": {
                    "x": 0.13,
                    "y": 0,
                    "z": 0,
                    "snap": True,
                    "snap_step": 0.25,
                    "frame_id": "world_xy",
                },
            },
        },
        headers=auth(editor_user),
    )

    assert r.status_code == 200
    new_id = r.json()["new_snapshot_id"]

    from app.models.audit_log import AuditLog  # adjust if needed

    evt = (
        db.query(AuditLog)
        .filter(AuditLog.action == "snapshot.transform")
        .filter(AuditLog.resource_id == new_id)
        .first()
    )

    assert evt is not None
    extra = evt.extra or {}

    assert extra.get("snap") is True
    assert extra.get("frame_id") == "world_xy"
    assert float(extra.get("snap_step")) == 0.25
