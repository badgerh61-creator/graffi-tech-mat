def test_assistant_call_is_audited(
    client,   # ← ADD THIS
    db,
    draft_snapshot,
    editor_user,
):
    client.post(
        f"/snapshots/{draft_snapshot.id}/assistant/tuning",
        headers=auth(editor_user),
        json={"mode": "inquiry"},
    )

    events = (
        db.query(AuditLog)
        .filter(AuditLog.action == "assistant.tuning.invoked")
        .all()
    )

    assert len(events) == 1

