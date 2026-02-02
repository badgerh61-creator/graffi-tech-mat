from app.models.read_view import ReadView
from app.services.presence_sessions import require_active_session
from app.services.audit import log_event

# 🔽 ADD THESE IMPORTS
from app.services.read_view_guard import (
    has_active_read_view,
    reject_mutation_from_read_view,
)


def open_read_view(*, db, snapshot, user):
    session = require_active_session(
        db=db,
        user=user,
        project_id=snapshot.project_id,
    )

    view = ReadView(
        snapshot_id=snapshot.id,
        user_id=user.id,
        session_id=session.id,
    )

    db.add(view)
    db.commit()

    # ✅ Audit contract compliant
    log_event(
        db=db,
        action="snapshot.view.opened",
        resource_type="snapshot",
        resource_id=snapshot.id,
        user_id=user.id,
        extra={
            "session_id": session.id,
        },
    )

    return view


# 🔽 ADD THIS EXPORT LIST
__all__ = [
    "open_read_view",
    "has_active_read_view",
    "reject_mutation_from_read_view",
]

