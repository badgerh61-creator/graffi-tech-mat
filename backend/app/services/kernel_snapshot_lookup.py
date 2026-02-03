from app.db.session import SessionLocal
from app.models.rendered_snapshot import RenderedSnapshot
from fastapi import HTTPException, status


def kernel_snapshot_lookup(*, snapshot_id: int):
    """
    Phase E — Kernel snapshot lookup (READ-ONLY).

    - No mutation
    - No authority
    - No caching
    """
    db = SessionLocal()

    snapshot = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot_id)
        .first()
    )

    if not snapshot:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Snapshot not found",
        )

    return snapshot

