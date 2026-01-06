"""
PHASE J WORKSPACE CONTRACT (READ-ONLY)

This file defines the canonical workspace payload delivered to the editor.

Rules:
- Snapshot-based visual truth only
- Deterministic ordering
- No mutation of snapshots
- No snapshot selection
- No engine side effects
- No implicit writes during editor boot

Any write operation MUST go through the Phase I mutation system.
"""

from sqlalchemy.orm import Session
from app.models.snapshot import RenderedSnapshot
from app.workspaces.normalize import normalize_snapshots


def build_project_workspace(db: Session, project_id: int):
    """
    PHASE J WORKSPACE BUILDER (READ-ONLY)

    - Assembles workspace payload
    - Applies Phase J.5 normalization
    - Does NOT mutate any state
    """

    snapshots = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.project_id == project_id)
        .order_by(RenderedSnapshot.created_at.desc())
        .all()
    )

    normalized_snapshots = normalize_snapshots(snapshots)

    return {
        "snapshots": normalized_snapshots,
        "meta": {
            "total": len(snapshots),
        },
    }

