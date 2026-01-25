from app.services import generate_surfaces_for_snapshot
from app.models.audit_log import AuditLog

def test_surface_generation_emits_audit_event(
    db,
    solved_draft_snapshot,
    editor_user,
):
    new_snapshot = generate_surfaces_for_snapshot(
        db=db,
        snapshot=solved_draft_snapshot,
        user=editor_user,
    )

    events = (
        db.query(AuditLog)
        .filter(AuditLog.action == "surface.generated")
        .filter(AuditLog.resource_id == new_snapshot.id)
        .all()
    )

    assert len(events) == 1

