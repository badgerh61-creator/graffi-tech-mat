from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib
import json

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.capabilities import require_capability
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot
from app.models.journal_entry import JournalEntry
from app.models.user import User

router = APIRouter(prefix="/scenes", tags=["scenes"])


@router.post("/{project_id}/mutations/save")
def save_scene(
    project_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    require_capability(
        db=db,
        user=user,
        project_id=project_id,
        capability="canTuneParameters",
    )

    scene_state = payload.get("scene_state")
    if scene_state is None:
        raise HTTPException(status_code=400, detail="scene_state required")

    canonical = json.dumps(scene_state, sort_keys=True)
    scene_hash = hashlib.sha256(canonical.encode()).hexdigest()

    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == project.id,
            RenderedSnapshot.scene_state_hash == scene_hash,
            RenderedSnapshot.status.in_(["pending", "completed"]),
        )
        .first()
    )

    if not snapshot:
        snapshot = RenderedSnapshot(
            project_id=project.id,
            scene_state_hash=scene_hash,
            render_profile="default",
            engine_version="phase-i",
            status="pending",
            created_by=user.id,
        )
        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)

    journal = JournalEntry(
        type="SAVE_SCENE",
        scene_id=project.id,
        snapshot_id=snapshot.id,
        actor_user_id=user.id,
        scene_hash=scene_hash,
    )

    db.add(journal)
    db.commit()

    return {
        "snapshot_id": snapshot.id,
        "scene_hash": scene_hash,
        "status": snapshot.status,
    }

