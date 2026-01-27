from app.models.audit_log import AuditLog
from app.services.mode_audit import audit_mode_transition

def test_mode_transition_emits_audit_event(db):
    audit_mode_transition(
        db=db,
        user_id=1,
        from_mode="editing",
        to_mode="review",
        snapshot_id=42,
    )

    events = (
        db.query(AuditLog)
        .filter(AuditLog.action == "studio.mode.transition")
        .all()
    )

    assert len(events) == 1

