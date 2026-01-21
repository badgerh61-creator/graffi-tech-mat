from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.db.session import SessionLocal


# =====================================================
# WRITE — AUDIT LOGGING (SAFE, NON-BLOCKING)
# =====================================================

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

    SAFETY GUARANTEES:
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


# =====================================================
# READ — AUDIT QUERY HELPER (PHASE 4.5 CONTRACT)
# =====================================================

def get_audit_events(
    db: Session | None = None,
    *,
    action: str | None = "snapshot.finalized",
    resource_type: str | None = None,
    resource_id: int | None = None,
):
    close_db = False

    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        q = db.query(AuditLog)

        if action is not None:
            q = q.filter(AuditLog.action == action)

        if resource_type is not None:
            q = q.filter(AuditLog.resource_type == resource_type)

        if resource_id is not None:
            q = q.filter(AuditLog.resource_id == resource_id)

        # 🔒 Phase 4.5 invariant — latest event only
        return q.order_by(AuditLog.created_at.desc()).limit(1).all()

    finally:
        if close_db:
            db.close()

