# backend/app/api/simulation_batch.py
from __future__ import annotations

import json
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user as get_current_user_maybe

from app.services.simulation_batch_runner import create_batch_and_run, get_batch

router = APIRouter(prefix="/simulation", tags=["simulation-batches"])


def require_auth_header(request: Request):
    """
    Tier 6S.7 requires STRICT auth.
    Your repo appears to allow a default/guest user, so we enforce header presence.
    """
    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return auth


def require_user(
    _auth=Depends(require_auth_header),
    user=Depends(get_current_user_maybe),
):
    # If header exists but token invalid, your get_current_user should raise 401/403.
    return user


@router.post("/batches")
def create_batch(
    body: Dict[str, Any],
    db: Session = Depends(get_db),
    user=Depends(require_user),
):
    snapshot_id = body.get("snapshot_id")
    engine_version = body.get("engine_version", "pseudo-v1")
    scenario_ids = body.get("scenario_ids") or []
    template_keys = body.get("template_keys") or []
    template_overrides = body.get("template_overrides") or {}

    if not isinstance(snapshot_id, int) or snapshot_id <= 0:
        raise HTTPException(422, "snapshot_id required")

    batch = create_batch_and_run(
        db=db,
        snapshot_id=snapshot_id,
        engine_version=engine_version,
        scenario_ids=scenario_ids,
        template_keys=template_keys,
        template_overrides=template_overrides,
        user_id=getattr(user, "id", 0) or 0,
    )

    return {
        "batch_id": int(batch.id),
        "status": batch.status,
        "run_ids": json.loads(batch.run_ids_json or "[]"),
        "artifact_ids": json.loads(batch.artifact_ids_json or "[]"),
    }


@router.get("/batches/{batch_id}")
def batch_status(
    batch_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_user),
):
    b = get_batch(db, batch_id=batch_id)
    if not b:
        raise HTTPException(404, "Batch not found")

    return {
        "batch_id": int(b.id),
        "status": b.status,
        "snapshot_id": int(b.snapshot_id),
        "engine_version": b.engine_version,
        "run_ids": json.loads(b.run_ids_json or "[]"),
        "artifact_ids": json.loads(b.artifact_ids_json or "[]"),
        "error": b.error,
    }
