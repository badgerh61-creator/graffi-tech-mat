from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib
import json

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot
from app.models.journal_entry import JournalEntry
from app.models.user import User

router = APIRouter(prefix="/scenes", tags=["scenes"])


@router.post("/{scene_id}/mutations/save")
def save_scene(
    scene_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Phase I.7 — Scene Save (Canonical, DB-Compatible)
    """

    # ---------------------------------------------------------
    # 1. Scene / Project existence
    # ---------------------------------------------------------
    project = db.get(Project, scene_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # ---------------------------------------------------------
    # 2. Archived project guard
    # ---------------------------------------------------------
    if project.archived_at is not None:
        raise HTTPException(status_code=403, detail="Project is archived")

    # ---------------------------------------------------------
    # 3. Authorization (Phase I.7 — role based)
    # ---------------------------------------------------------
    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(status_code=403, detail="Insufficient project permissions")

    # ---------------------------------------------------------
    # 4. Payload validation
    # ---------------------------------------------------------
    scene_state = payload.get("scene_state")
    if scene_state is None:
        raise HTTPException(status_code=400, detail="scene_state required")

    # ---------------------------------------------------------
    # 5. Deterministic hashing
    # ---------------------------------------------------------
    canonical_json = json.dumps(
        scene_state,
        sort_keys=True,
        separators=(",", ":"),
    )
    scene_hash = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    # ---------------------------------------------------------
    # 6. Duplicate snapshot detection
    # ---------------------------------------------------------
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == project.id,
            RenderedSnapshot.scene_state_hash == scene_hash,
            RenderedSnapshot.status.in_(["pending", "completed"]),
        )
        .first()
    )

    # ---------------------------------------------------------
    # 7. Snapshot creation (append-only)
    # ---------------------------------------------------------
    if not snapshot:
        snapshot = RenderedSnapshot(
            project_id=project.id,
            scene_state_hash=scene_hash,
            render_profile="default",
            engine_version="phase-i",
            status="completed",  # ✅ always completed in dev
            created_by=user.id,
        )
        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)
    else:
        # 🔥 FIX: upgrade pending → completed
        if snapshot.status == "pending":
            snapshot.status = "completed"
            db.commit()
            db.refresh(snapshot)

    # ---------------------------------------------------------
    # 8. Journaling (Phase I.7 + Phase K safe)
    # ---------------------------------------------------------
    journal = JournalEntry(
        # Phase K required fields
        project_id=project.id,
        mutation_type="SAVE_SCENE",
        snapshot_before=snapshot.id,
        snapshot_after=snapshot.id,
        actor_id=user.id,

        # Phase I.7 legacy fields (tests rely on these)
        type="SAVE_SCENE",
        scene_id=project.id,
        snapshot_id=snapshot.id,
        actor_user_id=user.id,
        scene_hash=scene_hash,
    )
    db.add(journal)
    db.commit()

    # ---------------------------------------------------------
    # 9. Response
    # ---------------------------------------------------------
    return {
        "snapshot_id": snapshot.id,
        "status": snapshot.status,
    }
