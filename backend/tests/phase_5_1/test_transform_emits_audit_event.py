from app.services import apply_transform

def test_transform_emits_audit_event(
    db,
    draft_snapshot,
    editor_user,
):
    apply_transform(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
        operation="translate",
        target_id="body.root",
        params={"x": 1, "y": 0, "z": 0},
    )

    events = get_audit_events(action="snapshot.transform")
    assert len(events) == 1

