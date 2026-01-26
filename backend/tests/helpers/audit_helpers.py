from app.models.audit import AuditLog

def get_audit_events(db, *, action):
    return (
        db.query(AuditLog)
        .filter(AuditLog.action == action)
        .all()
    )

