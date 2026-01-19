# app/api/mutations/mutations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.asset import Asset
from app.models.model import ModelRecord
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.models.mutation_journal import MutationJournal

from app.services.capabilities import require_capability
from app.services.mutations.rename_asset import RenameAssetAdapter


router = APIRouter(prefix="/mutations", tags=["mutations"])

# ============================================================
# PHASE I.1 — Rename Asset
# ============================================================

@router.post("/rename-asset")
def rename_asset(
    *,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    payload: dict,
):
    target_id = payload.get("targetId")
    previous_name = payload.get("previousName")
    next_name = payload.get("nextName")
    reason = payload.get("reason")

    if not target_id or not previous_name or not next_name:
        raise HTTPException(status_code=400, detail="Invalid payload")

    asset = db.query(Asset).filter(Asset.id == target_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    model = db.query(ModelRecord).filter(ModelRecord.id == asset.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    # 🔐 Canonical gate
    require_capability(
        db=db,
        user=user,
        project_id=model.owner_id,
        capability="canModifyBody",
    )

    if asset.filename != previous_name:
        raise HTTPException(status_code=409, detail="Stale asset state")

    journal = MutationJournal(
        intent_type="RenameAsset",
        target_type="asset",
        target_id=asset.id,
        before_state={"filename": previous_name},
        after_state={"filename": next_name},
        issued_by_user_id=user.id,
        reason=reason,
    )

    RenameAssetAdapter.execute(db, asset=asset, next_name=next_name)
    db.add(journal)
    db.commit()

    return {
        "status": "ok",
        "assetId": asset.id,
        "newName": next_name,
    }


# ============================================================
# PHASE I.3 — Set Active Snapshot (PRIVATE)
# ============================================================

@router.post("/set-active-snapshot")
def set_active_snapshot(
    *,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    payload: dict,
):
    project_id = payload.get("projectId")
    next_snapshot_id = payload.get("nextSnapshotId")

    if not project_id or not next_snapshot_id:
        raise HTTPException(status_code=400, detail="Invalid payload")

    # 🔐 Capability gate (editor/admin only)
    require_capability(
        db=db,
        user=user,
        project_id=project_id,
        capability="canDecorateExterior",
    )

    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == next_snapshot_id,
            RenderedSnapshot.project_id == project_id,
            RenderedSnapshot.status == SnapshotStatus.COMPLETED,
        )
        .first()
    )
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    project = db.get(Project, project_id)
    project.active_snapshot_id = snapshot.id
    db.commit()

    return {
        "status": "ok",
        "activeSnapshotId": snapshot.id,
    }

