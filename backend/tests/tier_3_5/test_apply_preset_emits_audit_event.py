from app.services.decor_application import apply_decor_preset
from app.models.audit import AuditLog


def test_apply_preset_emits_audit_event(
    db,
    draft_snapshot,
    decor_preset,
    editor_user,
):
    new_snapshot = apply_decor_preset(
        db=db,
        snapshot=draft_snapshot,
        preset=decor_preset,
        user=editor_user,
    )

    events = (
        db.query(AuditLog)
        .filter(AuditLog.action == "snapshot.decor_preset_applied")
        .filter(AuditLog.resource_id == new_snapshot.id)
        .all()
    )

    assert len(events) == 1

