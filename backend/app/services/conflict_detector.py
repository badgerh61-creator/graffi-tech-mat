# backend/app/services/conflict_detector.py

from app.models.rendered_snapshot import RenderedSnapshot


class ConflictResult:
    def __init__(self, is_conflicted: bool, reason: str | None = None):
        self.is_conflicted = is_conflicted
        self.reason = reason


def get_latest_snapshot(db, project_id: int):
    return (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == project_id,
            RenderedSnapshot.status == "completed",
        )
        .order_by(RenderedSnapshot.created_at.desc())
        .first()
    )


def detect_conflict(*, db, snapshot, user) -> ConflictResult:
    """
    Phase U.3 — Conflict Detection (READ-ONLY, AUTHORITATIVE)
    """

    if snapshot.status != "draft":
        return ConflictResult(False)

    latest = get_latest_snapshot(db, snapshot.project_id)

    if latest is None:
        return ConflictResult(False)

    if snapshot.parent_snapshot_id != latest.id:
        return ConflictResult(
            is_conflicted=True,
            reason="stale_parent",
        )

    return ConflictResult(False)

