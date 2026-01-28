from datetime import datetime
from app.models.audit_log import AuditLog


def create_command(
    *,
    db,
    snapshot,
    operation: str,
    target_id: str,
    params: dict,
    user,
):
    """
    Phase 5.5 / Phase U compatibility stub.

    Records a command execution as an audit-backed event.
    """

    event = AuditLog(
        user_id=user.id,
        action="snapshot.transform",
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={
            "operation": operation,
            "target_id": target_id,
            "params": params,
        },
        created_at=datetime.utcnow(),
    )

    db.add(event)
    return event

