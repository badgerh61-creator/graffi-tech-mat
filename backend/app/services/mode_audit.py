from app.services import audit

def audit_mode_transition(*, db, user_id, from_mode, to_mode, snapshot_id):
    audit.log_event(
        db,
        user_id=user_id,
        action="studio.mode.transition",
        resource_type="snapshot",
        resource_id=snapshot_id,
        extra={
            "from": from_mode,
            "to": to_mode,
        },
    )

