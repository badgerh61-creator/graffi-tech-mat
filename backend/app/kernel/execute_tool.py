from fastapi import HTTPException

from app.kernel.t_authority import require_draft_authority
from app.services.conflict_detector import detect_conflict
from app.services.snapshot_mutations import apply_transform
from app.services.draft_lock_service import get_draft_lock
from app.models.conflict import SnapshotConflict


def execute_tool(*, db, user, snapshot, tool: str, params: dict):
    # 1️⃣ Draft ownership (local, cheap)
    lock = get_draft_lock(db=db, snapshot=snapshot)
    if not lock or lock.user_id != user.id:
        raise HTTPException(403, "Not draft owner")

    # 2️⃣ Explicit conflict marker (Phase U.3 — authoritative)
    explicit = (
        db.query(SnapshotConflict)
        .filter(SnapshotConflict.snapshot_id == snapshot.id)
        .first()
    )
    if explicit:
        raise HTTPException(409, "Snapshot conflict detected")

    # 3️⃣ Structural conflict (frozen U.3 logic)
    structural = detect_conflict(db=db, snapshot=snapshot, user=user)
    if structural.is_conflicted:
        raise HTTPException(409, f"Snapshot conflict: {structural.reason}")

    # 4️⃣ Temporal authority (session + lifecycle)
    require_draft_authority(db=db, user=user, snapshot=snapshot)

    # 5️⃣ Tool registry
    if tool not in {"translate", "scale", "rotate"}:
        raise HTTPException(422, "Invalid tool")

    return apply_transform(
        db=db,
        snapshot=snapshot,
        user=user,
        operation=tool,
        target_id=params.get("target_id", "default"),
        params=params,
    )

