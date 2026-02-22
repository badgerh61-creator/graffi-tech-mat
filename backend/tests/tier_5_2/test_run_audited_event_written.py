def test_run_audited_event_written(db, client, draft_snapshot, editor_user):
    r = client.post(
        f"/snapshots/{draft_snapshot.id}/testing/run",
        headers=auth(editor_user),
        json={"scenario_id": "track-dry-day-v1"},
    )
    assert r.status_code == 200

    ev = (
        db.query(AuditLog)
        .filter(AuditLog.action == "testing.run.requested")
        .filter(AuditLog.resource_type == "snapshot")
        .filter(AuditLog.resource_id == draft_snapshot.id)
        .first()
    )
    assert ev is not None
