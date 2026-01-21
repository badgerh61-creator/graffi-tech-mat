def test_finalize_emits_audit_event(
    db,
    draft_snapshot,
    editor_user,
):
    finalize_snapshot(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
    )

    events = get_audit_events(action="snapshot.finalized")
    assert len(events) == 1

