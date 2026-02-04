from app.services.image_exporter import create_image_export

def test_export_emits_audit_event(
    db,
    completed_snapshot,
    editor_user,
):
    create_image_export(
        db=db,
        snapshot=completed_snapshot,
        user=editor_user,
        format="png",
        resolution="medium",
    )

    events = get_audit_events(action="snapshot.export.image")
    assert len(events) == 1

