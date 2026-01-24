from sqlalchemy.orm import Session
from app.models.rendered_snapshot import RenderedSnapshot


def get_snapshot_by_id(db: Session, snapshot_id: int):
    """
    Legacy snapshot lookup (Phase 4.x / Phase I.4 compatibility).

    Contract:
    - Return snapshot if found
    - Return None if not found
    - NEVER raise
    """
    return (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot_id)
        .first()
    )

