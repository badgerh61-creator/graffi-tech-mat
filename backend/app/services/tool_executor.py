from app.services.read_view_guard import reject_mutation_from_read_view
from app.services.snapshot_guard import require_draft_snapshot
from app.services.studio_kernel_guard import enforce_tool_authority

def execute_tool(*, db, user, snapshot, tool, params):
    # 1️⃣ Phase U.5 — Read views can never mutate
    reject_mutation_from_read_view(
        db=db,
        snapshot=snapshot,
        user=user,
    )

    # 2️⃣ Phase 4 / 5 — Only drafts are mutable
    require_draft_snapshot(snapshot)

    # 3️⃣ Phase T — Station / tool / flow authority
    enforce_tool_authority(
        db=db,
        user=user,
        snapshot=snapshot,
        tool=tool,
    )

    # 4️⃣ Execute tool (guaranteed safe)
    return tool.execute(
        db=db,
        snapshot=snapshot,
        user=user,
        params=params,
    )

