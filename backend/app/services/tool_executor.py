# backend/app/services/tool_executor.py

from app.services.snapshot_guard import require_draft_snapshot
from app.services.studio_kernel_guard import enforce_tool_authority
from app.services.tool_registry import get_tool
from app.services.audit import log_event


from app.services.presence_sessions import require_active_session

def execute_tool(*, db, user, snapshot, tool, params):
    tool_obj = get_tool(tool) if isinstance(tool, str) else tool

    # 1️⃣ Lifecycle
    require_draft_snapshot(snapshot=snapshot)

    # 2️⃣ Kernel authority (FULL)
    enforce_tool_authority(
        db=db,
        user=user,
        snapshot=snapshot,
        tool=tool_obj,
    )

    # 🔥 Phase U.S — REVALIDATE SESSION BEFORE COMMIT
    require_active_session(
        db=db,
        user=user,
        project_id=snapshot.project_id,
        snapshot_id=snapshot.id,
    )

    # 3️⃣ Execute (mutation boundary)
    new_snapshot = tool_obj.execute(
        db=db,
        snapshot=snapshot,
        user=user,
        params=params,
    )

    log_event(
        db=db,
        action="snapshot.mutated",
        resource_type="snapshot",
        resource_id=new_snapshot.id,
        user_id=user.id,
        extra={
            "parent_snapshot_id": snapshot.id,
            "tool": tool_obj.name,
        },
    )

    return new_snapshot

