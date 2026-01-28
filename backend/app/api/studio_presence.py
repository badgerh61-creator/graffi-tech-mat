from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.studio_presence import StudioPresence

router = APIRouter(
    prefix="/projects/{project_id}/presence",
    tags=["studio-presence"],
)


@router.post("/join")
def join_presence(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    presence = StudioPresence(
        user_id=user.id,
        project_id=project_id,
    )

    db.add(presence)
    db.commit()

    return {"status": "joined"}


@router.post("/leave")
def leave_presence(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    (
        db.query(StudioPresence)
        .filter(
            StudioPresence.user_id == user.id,
            StudioPresence.project_id == project_id,
        )
        .delete()
    )

    db.commit()
    return {"status": "left"}

