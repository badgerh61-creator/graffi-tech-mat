from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


def log_event(
    db: Session,
    *,
    user_id: int | None,
    action: str,
    resource_type: str,
    resource_id: int | None = None,
    extra: dict | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
):
    """
    Write an audit log entry.

    This function is SAFE:
    - Never raises outward
    - Never blocks main request
    - Rolls back on failure
    """
    try:
        entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            extra=extra,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.add(entry)
        db.commit()
    except Exception:
        db.rollback()

