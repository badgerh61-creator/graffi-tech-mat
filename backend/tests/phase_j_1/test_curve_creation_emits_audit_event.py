from app.services.curve_creator import create_curve
from app.models.audit_log import AuditLog

def test_curve_creation_emits_audit_event(
    db,
    draft_snapshot,
    editor_user,
):
    new_snapshot, curve = create_curve(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
        curve_type="line",
        reference_plane_id="front",
        params={"x1": 0, "y1": 0, "x2": 50, "y2": 0},
        constraints=[],
    )

    events = db.query(AuditLog).filter(
        AuditLog.action == "curve.create",
        AuditLog.resource_id == curve.id,
    ).all()

    assert len(events) == 1

