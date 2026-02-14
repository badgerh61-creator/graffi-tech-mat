# backend/app/studio/structural_guards.py

from app.studio.kernel_errors import KernelRejection
from app.services.mode_resolver import resolve_mode
from app.services.mode_guard import require_mode_allows_tool


ALLOWED_STATIONS = {
    "geometry",
    "curve",
    "panel",
    "validation",
    "review",
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
# Structural Guards (Phase T)
# =====================================================

def require_tool_exists(tool):
    if tool not in ALLOWED_TOOLS:
        raise KernelRejection(reason="tool")


def require_station_exists(station):
    if station not in ALLOWED_STATIONS:
        raise KernelRejection(reason="station")


def require_station_tool_flow(station, tool):
    # review station is reserved for finalize
    if station == "review" and tool != "finalize":
        raise KernelRejection(reason="station")

    # finalize tool is only allowed in review
    if tool == "finalize" and station != "review":
        raise KernelRejection(reason="flow")


def require_snapshot_allows(snapshot, tool):
    """
    Lifecycle enforcement belongs to structural layer.
    Draft required unless tool is finalize.
    """
    if tool != "finalize" and snapshot.status != "draft":
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


def require_user_capability(user):
    if user.role not in ("editor", "owner", "admin"):
        raise KernelRejection(reason="capability")


# =====================================================
# Execution Delegate (Pure)
# =====================================================

def apply_tool(*, db, snapshot, user, operation, params):
    new_snapshot = snapshot.clone_for_mutation(
        created_by=user.id,
    )
    db.add(new_snapshot)
    db.commit()
    return new_snapshot

