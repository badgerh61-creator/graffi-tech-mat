from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.session import get_db
from app.api.deps import require_admin
from app.models.audit_log import AuditLog

router = APIRouter(
    prefix="/admin/audit",
    tags=["admin-audit"],
)


@router.get("/")
def list_audit_logs(
    page: int = 1,
    limit: int = 200,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    q = db.query(AuditLog)

    total = q.count()

    logs = (
        q.order_by(desc(AuditLog.created_at))
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "items": [
            {
                "id": l.id,
                "user_id": l.user_id,
                "action": l.action,
                "resource_type": l.resource_type,
                "resource_id": l.resource_id,
                "extra": l.extra,
                "ip_address": l.ip_address,
                "user_agent": l.user_agent,
                "created_at": l.created_at,
            }
            for l in logs
        ],
        "page": page,
        "limit": limit,
        "total": total,
    }

