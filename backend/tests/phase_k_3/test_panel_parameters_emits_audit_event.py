from app.services import apply_panel_parameters
from app.models.audit_log import AuditLog

def test_panel_parameters_emits_audit_event(
    db,
    segmented_draft_snapshot,
    editor_user,
):
    new_snapshot = apply_panel_parameters(
        db=db,
        snapshot=segmented_draft_snapshot,
        user=editor_user,
        panel_id="panel-1",
        parameters={"rake_angle": 7.0},
    )

    events = db.query(AuditLog).filter(
        AuditLog.action == "panel.parameters.applied",
        AuditLog.resource_id == new_snapshot.id,
    ).all()

    assert len(events) == 1

