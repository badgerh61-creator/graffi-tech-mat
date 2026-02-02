# backend/app/services/tool_executor.py

from app.services.read_view_guard import reject_mutation_from_read_view
from app.services.snapshot_guard import require_draft_snapshot
from app.services.studio_kernel_guard import enforce_tool_authority
from app.services.tool_registry import get_tool
from app.services.audit import log_event


def execute_tool(*, db, user, snapshot, tool, params):
    tool_obj = get_tool(tool) if isinstance(tool, str) else tool

    # 1️⃣ Phase 4 / 5 — Only drafts are mutable
    require_draft_snapshot(snapshot=snapshot)

    # 2️⃣ Phase U.5 — Read views block NON-OWNERS only
    reject_mutation_from_read_view(
        db=db,
        snapshot=snapshot,
        user=user,
    )

    # 3️⃣ Phase T + U — Session + ownership + conflict authority
    enforce_tool_authority(
        db=db,
        user=user,
        snapshot=snapshot,
        tool=tool_obj,
    )

    # 4️⃣ Execute tool
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

