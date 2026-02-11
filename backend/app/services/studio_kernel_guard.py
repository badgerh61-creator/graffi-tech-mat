# backend/app/services/studio_kernel_guard.py

from fastapi import HTTPException

from app.services.audit import log_event
from app.services.session_guard import require_active_session
from app.services.conflict_guard import require_no_conflict
from app.services.read_view_guard import reject_mutation_from_read_view
from app.services.draft_lock_service import require_draft_owner


def enforce_tool_authority(*, db, user, snapshot, tool):
    """
    Phase T — FINAL authority gate.

    ORDER IS ABSOLUTE:
    1. Session
    2. Conflict
    3. Read view
    4. Ownership
    """

    try:
        # 1️⃣ Session ALWAYS first
        require_active_session(
            db=db,
            user=user,
            project_id=snapshot.project_id,
            snapshot_id=snapshot.id,
        )

        if not tool.is_mutating:
            return

        # 2️⃣ Conflict dominates everything
        require_no_conflict(
            db=db,
            snapshot=snapshot,
            user=user,
        )

        # 3️⃣ Read view (owners pass through)
        reject_mutation_from_read_view(
            db=db,
            snapshot=snapshot,
            user=user,
        )

        # 4️⃣ Ownership (last)
        require_draft_owner(
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

