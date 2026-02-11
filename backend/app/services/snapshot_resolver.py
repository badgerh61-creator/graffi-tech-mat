from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot


def resolve_active_snapshot_for_boot(db, project_id):
    """
    Resolve the snapshot to use for editor boot.
    Read-only. No mutations allowed.
    """

    project = db.get(Project, project_id)
    if not project:
        return None

    # 1. Try active snapshot first
    if project.active_snapshot_id:
        active = (
            db.query(RenderedSnapshot)
            .filter(
                RenderedSnapshot.id == project.active_snapshot_id,
                RenderedSnapshot.status == "completed",
            )
            .first()
        )
        if active:
            return active

    # 2. Fallback: most recent completed snapshot
    return (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == project_id,
            RenderedSnapshot.status == "completed",
        )
        .order_by(RenderedSnapshot.created_at.desc())
        .first()
    )

