"""
PHASE J.5 — WORKSPACE SNAPSHOT QUERY PRIMITIVE

Responsibilities:
- Read-only snapshot access
- Default exclusion of failed/pending snapshots
- Deterministic ordering (NEWEST FIRST)
- NO mutation
- NO selection logic
"""

from app.models.rendered_snapshot import RenderedSnapshot


def get_workspace_snapshots(
    *,
    db,
    project_id: int,
    include_failed: bool = False,
):
    """
    Return workspace snapshots according to Phase J.5 rules.

    Default behavior:
    - Only `completed` snapshots are returned
    - Ordering is deterministic (created_at DESC, id DESC)

    include_failed=True is reserved for privileged callers
    (admin / owner), but filtering is still enforced here.
    """

    query = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.project_id == project_id)
    )

    if not include_failed:
        query = query.filter(RenderedSnapshot.status == "completed")

    return (
        query
        .order_by(
            RenderedSnapshot.created_at.desc(),
            RenderedSnapshot.id.desc(),
        )
        .all()
    )

