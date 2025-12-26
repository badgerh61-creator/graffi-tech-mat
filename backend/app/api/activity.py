from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.audit_log import AuditLog
from app.models.model_permission import ModelPermission
from app.models.model import ModelRecord

router = APIRouter(
    prefix="/activity",
    tags=["activity"],
)


@router.get("/")
def list_activity(
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Activity feed for the current user.
    Includes:
    - models they own
    - models they collaborate on
    - their own actions
    """

    model_ids_subq = (
        db.query(ModelRecord.id)
        .outerjoin(
            ModelPermission,
            ModelPermission.model_id == ModelRecord.id,
        )
        .filter(
            (ModelRecord.owner_id == user.id)
            | (ModelPermission.user_id == user.id)
        )
        .subquery()
    )

    q = (
        db.query(AuditLog)
        .filter(
            (AuditLog.user_id == user.id)
            | (
                (AuditLog.resource_type == "model")
                & (AuditLog.resource_id.in_(model_ids_subq))
            )
        )
    )

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
                "created_at": l.created_at,
            }
            for l in logs
        ],
        "page": page,
        "limit": limit,
        "total": total,
    }

