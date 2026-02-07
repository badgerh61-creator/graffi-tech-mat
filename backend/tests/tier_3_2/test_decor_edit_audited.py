def test_decor_edit_emits_audit_event(
    db,
    draft_snapshot,
    editor_user,
):
    new_snapshot = apply_decor_change(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
        operation="decor.replace_preset",
        target_id="seat-1",
        params={"preset": "sport"},
    )

    events = get_audit_events(action="snapshot.decor.edit")
    assert len(events) == 1
    assert events[0].resource_id == new_snapshot.id

