from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus

from app.services.capabilities import require_capability
from app.services.journal import write_journal_entry

from app.api.mutations.decor.schemas import ApplyExteriorDecalPayload
from app.validation.decor.exterior import validate_apply_decal
from app.validation.decor.errors import DecorValidationError

import hashlib
import json

router = APIRouter(
    prefix="/mutations/decor/exterior",
    tags=["mutations"],
)


@router.post("/apply-decal")
def apply_decal(
    *,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    payload: ApplyExteriorDecalPayload,
):
    # ---------------------------------------------------------
    # Capability gate (Phase K.0)
    # ---------------------------------------------------------
    require_capability(
        db=db,
        user=user,
        project_id=payload.project_id,
        capability="canDecorateExterior",
    )

    project = db.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    base_snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == payload.snapshot_base_id,
            RenderedSnapshot.project_id == payload.project_id,
        )
        .first()
    )

    if not base_snapshot:
        raise HTTPException(status_code=404, detail="Base snapshot not found")

    # ---------------------------------------------------------
    # Canonical validation layer (MANDATORY)
    # ---------------------------------------------------------
    try:
        validate_apply_decal(
            capabilities={"canDecorateExterior": True},
            snapshot=base_snapshot,
            decal=type("Decal", (), {"is_exterior": True})(),  # placeholder
            target=payload.target,
        )
    except DecorValidationError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "error": e.error_code,
                "message": e.message,
            },
        )

    # ---------------------------------------------------------
    # Deterministic state transform (PURE)
    # ---------------------------------------------------------
    new_decor_state = {
        **(base_snapshot.decor_state or {}),
        "applied_decal": {
            "decal_id": payload.decal_id,
            "target": payload.target,
        },
    }

    new_scene_state_hash = hashlib.sha256(
        json.dumps(
            {
                "base_scene_state_hash": base_snapshot.scene_state_hash,
                "decor_state": new_decor_state,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    # ---------------------------------------------------------
    # Deterministic deduplication (Phase I / J)
    # ---------------------------------------------------------
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == payload.project_id,
            RenderedSnapshot.scene_state_hash == new_scene_state_hash,
            RenderedSnapshot.render_profile == base_snapshot.render_profile,
            RenderedSnapshot.engine_version == base_snapshot.engine_version,
        )
        .first()
    )

    if not snapshot:
        snapshot = RenderedSnapshot(
            project_id=payload.project_id,
            scene_state_hash=new_scene_state_hash,
            render_profile=base_snapshot.render_profile,
            engine_version=base_snapshot.engine_version,
            decor_state=new_decor_state,
            tuning_state=base_snapshot.tuning_state,
            body_state=base_snapshot.body_state,
            status=SnapshotStatus.PENDING,
            created_by=user.id,
        )
        db.add(snapshot)
        db.flush()

    # ---------------------------------------------------------
    # Journaling (MANDATORY)
    # ---------------------------------------------------------
    write_journal_entry(
        db=db,
        intent_type="decor.exterior.apply-decal",
        target_type="snapshot",
        target_id=snapshot.id,
        before_state={
            "snapshot_id": base_snapshot.id,
            "decor_state": base_snapshot.decor_state,
        },
        after_state={
            "snapshot_id": snapshot.id,
            "decor_state": new_decor_state,
        },
        issued_by_user_id=user.id,
    )

    db.commit()
    return {"snapshot_id": snapshot.id}

