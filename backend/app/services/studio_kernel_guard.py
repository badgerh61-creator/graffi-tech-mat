# backend/app/services/studio_kernel_guard.py

from fastapi import HTTPException

from app.services.audit import log_event
from app.services.session_guard import require_active_session
from app.services.draft_lock_service import require_draft_owner
from app.services.conflict_guard import require_no_conflict


def enforce_tool_authority(*, db, user, snapshot, tool):
    """
    Phase T — Studio Kernel Authority Gate (FROZEN CONTRACT)

    Order is authoritative:
    1. Active session
    2. Draft ownership (if mutating)
    3. Conflict absence (if mutating)
    """

    try:
        require_active_session(
            db=db,
            user=user,
            project_id=snapshot.project_id,
        )

        if tool.is_mutating:
            require_draft_owner(
                db=db,
                snapshot=snapshot,
                user=user,
            )
            require_no_conflict(
                db=db,
                snapshot=snapshot,
                user=user,
            )

    except HTTPException:
        log_event(
            db=db,
            action="authority.violation",
            resource_type="snapshot",
            resource_id=snapshot.id,
            user_id=user.id,
            extra={"tool": tool.name},
        )
        raise

