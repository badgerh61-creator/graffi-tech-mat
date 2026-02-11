from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import get_db
from app.api.deps import require_admin
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.asset import Asset, AssetStatus
from app.worker.tasks import process_asset_task
from app.services import audit
from app import crud

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


# =========================
# USERS
# =========================

@router.get("/users", response_model=list[dict])
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    users = db.query(User).order_by(User.id).all()

    return [
        {
            "id": u.id,
            "email": u.email,
            "is_admin": u.is_admin,
            "is_active": u.is_active,
            "created_at": u.created_at,
        }
        for u in users
    ]


@router.post("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    if admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin cannot deactivate themselves",
        )

    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.is_active = False

    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked.is_(False),
    ).update({RefreshToken.revoked: True})

    db.commit()
    return {"detail": "User deactivated and sessions revoked"}


@router.post("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.is_active = True
    db.commit()
    return {"detail": "User activated"}


# =========================
# SESSIONS
# =========================

@router.post("/users/{user_id}/revoke-sessions")
def revoke_user_sessions(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    count = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked.is_(False),
        )
        .update({RefreshToken.revoked: True})
    )

    db.commit()
    return {
        "detail": "Sessions revoked",
        "revoked_count": count,
    }


# =========================
# PHASE 10.3 — ASSET RECOVERY
# =========================

@router.get("/assets/failed")
def list_failed_assets_admin(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return db.query(Asset).filter(
        Asset.status == AssetStatus.failed
    ).all()


@router.get("/assets/stuck")
def list_stuck_assets_admin(
    older_than_minutes: int = 10,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    cutoff = datetime.utcnow() - timedelta(minutes=older_than_minutes)

    return (
        db.query(Asset)
        .filter(
            Asset.status.in_(
                [AssetStatus.uploading, AssetStatus.processing]
            ),
            Asset.status_updated_at < cutoff,
        )
        .all()
    )


@router.post("/assets/{asset_id}/retry")
def retry_asset_admin(
    asset_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(404, "Asset not found")

    crud.admin_retry_asset(db, asset=asset)
    process_asset_task.delay(asset.id)

    audit.log_event(
        db,
        user_id=admin.id,
        action="asset.retry",
        resource_type="asset",
        resource_id=asset.id,
    )

    return {"detail": "Asset requeued for processing"}


@router.post("/assets/{asset_id}/fail")
def force_fail_asset_admin(
    asset_id: int,
    reason: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(404, "Asset not found")

    crud.admin_force_fail_asset(
        db,
        asset=asset,
        reason=reason,
    )

    audit.log_event(
        db,
        user_id=admin.id,
        action="asset.force_fail",
        resource_type="asset",
        resource_id=asset.id,
        extra={"reason": reason},
    )

    return {"detail": "Asset permanently failed"}

