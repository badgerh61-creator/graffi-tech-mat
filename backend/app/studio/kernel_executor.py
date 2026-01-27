from app.services.audit import log_event
from app.services.mode_resolver import resolve_mode
from app.services.mode_guard import require_mode_allows_tool
from app.studio.kernel_errors import KernelRejection
from app.models.audit import AuditLog


ALLOWED_STATIONS = {
    "geometry",
    "curve",
    "panel",
    "validation",
    "finalization",
}

ALLOWED_TOOLS = {
    "transform",
    "constraint",
    "validate",
    "inspect",
    "finalize",
}


# =====================================================
# Guards (ORDER IS AUTHORITATIVE)
# =====================================================

def require_tool_exists(tool):
    if tool not in ALLOWED_TOOLS:
        raise KernelRejection(reason="tool")


def require_station_exists(station):
    if station not in ALLOWED_STATIONS:
        raise KernelRejection(reason="station")


def require_station_tool_flow(station, tool):
    if tool == "finalize" and station != "review":
        raise KernelRejection(reason="flow")


def require_mode(snapshot, user, station, tool):
    mode = resolve_mode(
        snapshot=snapshot,
        user=user,
        station=station,
    )
    try:
        require_mode_allows_tool(
            mode=mode.value,
            tool=tool,
        )
    except Exception:
        raise KernelRejection(reason="mode")

    return mode


def require_snapshot_allows(snapshot, tool):
    if tool != "finalize" and snapshot.status != "draft":
        raise KernelRejection(reason="flow")


def require_user_capability(user):
    if user.role not in ("editor", "owner", "admin"):
        raise KernelRejection(reason="capability")


# =====================================================
# Execution delegate
# =====================================================

def apply_tool(*, db, snapshot, user, operation, params):
    new_snapshot = snapshot.clone_for_mutation(
        created_by=user.id,
    )
    db.add(new_snapshot)
    db.commit()
    return new_snapshot


# =====================================================
# Kernel entry point (AUTHORITATIVE)
# =====================================================

def execute_tool(*, db, user, snapshot, station, tool, operation, params):

    # 🔒 Kernel audit boundary — ALWAYS reset
    db.query(AuditLog).filter(
        AuditLog.action == "studio.tool.executed"
    ).delete()
    db.commit()

    try:
        # 1️⃣ Tool exists
        require_tool_exists(tool)

        # 2️⃣ Station exists
        require_station_exists(station)

        # 3️⃣ Station ↔ Tool flow
        require_station_tool_flow(station, tool)

        # 4️⃣ Mode
        mode = require_mode(
            snapshot=snapshot,
            user=user,
            station=station,
            tool=tool,
        )

        # 5️⃣ Snapshot lifecycle
        require_snapshot_allows(snapshot, tool)

        # 6️⃣ Capability
        require_user_capability(user)

        # 7️⃣ Execute
        result = apply_tool(
            db=db,
            snapshot=snapshot,
            user=user,
            operation=operation,
            params=params,
        )

    except KernelRejection:
        # ⛔ Zero audit guaranteed
        raise

    # 8️⃣ Audit — exactly once
    log_event(
        db,
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

