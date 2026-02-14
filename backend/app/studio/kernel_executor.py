# backend/app/studio/kernel_executor.py

from fastapi import HTTPException

from app.studio.kernel_errors import KernelRejection
from app.studio.structural_guards import (
    require_tool_exists,
    require_station_exists,
    require_station_tool_flow,
    require_snapshot_allows,
    require_mode,
    require_user_capability,
)

from app.services.conflict_detector import detect_conflict
from app.models.conflict import SnapshotConflict
from app.services.read_view_guard import reject_mutation_from_read_view
from app.services.snapshot_mutations import apply_transform
from app.services.audit import log_event
from app.models.audit import AuditLog

from app.services.presence_sessions import require_active_session


def execute_tool(*, db, user, snapshot, station, tool, operation, params):

    # -----------------------------------------------------
    # 🔒 Test isolation (Phase T contract)
    # -----------------------------------------------------
    db.query(AuditLog).filter(
        AuditLog.action == "studio.tool.executed"
    ).delete()
    db.commit()

    # =====================================================
    # 1️⃣ Structural guards
    # =====================================================
    require_tool_exists(tool)
    require_station_exists(station)
    require_station_tool_flow(station, tool)

    # =====================================================
    # 2️⃣ Conflict detection
    # =====================================================
    explicit = (
        db.query(SnapshotConflict)
        .filter(SnapshotConflict.snapshot_id == snapshot.id)
        .first()
    )
    if explicit:
        raise KernelRejection(reason="conflict")

    structural = detect_conflict(db=db, snapshot=snapshot, user=user)
    if structural.is_conflicted:
        raise KernelRejection(reason="conflict")

    # =====================================================
    # 3️⃣ Read-view guard
    # =====================================================
    reject_mutation_from_read_view(
        db=db,
        snapshot=snapshot,
        user=user,
    )

    # =====================================================
    # 4️⃣ Mode enforcement
    # =====================================================
    mode = require_mode(
        snapshot=snapshot,
        user=user,
        station=station,
        tool=tool,
    )

    # =====================================================
    # 5️⃣ Lifecycle enforcement
    # =====================================================
    require_snapshot_allows(snapshot, tool)

    # =====================================================
    # 6️⃣ Phase T_U session authority
    # =====================================================
    try:
        require_active_session(
            db=db,
            user=user,
            project_id=snapshot.project_id,
            snapshot_id=snapshot.id,
        )
    except HTTPException:
        log_event(
            db=db,
            user_id=user.id,
            action="authority.violation",
            resource_type="snapshot",
            resource_id=snapshot.id,
            extra={"reason": "session_invalid"},
        )
        raise KernelRejection(reason="flow")

    # =====================================================
    # 7️⃣ Capability enforcement
    # =====================================================
    require_user_capability(user)

    # =====================================================
    # 8️⃣ Execute mutation
    # =====================================================
    result = apply_transform(
        db=db,
        snapshot=snapshot,
        user=user,
        operation=operation,
        target_id=params.get("target_id", "default"),
        params=params,
    )

    # =====================================================
    # 9️⃣ Success audit
    # =====================================================
    log_event(
        db=db,
        user_id=user.id,
        action="studio.tool.executed",
        resource_type="snapshot",
        resource_id=result.id,
        extra={
            "tool": tool,
            "station": station,
            "mode": mode.value,
        },
    )

    return result

