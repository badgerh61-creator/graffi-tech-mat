# backend/app/services/tool_availability.py

from app.services.mode_resolver import resolve_mode
from app.studio.tool_registry import get_all_tools


def get_tool_availability(*, user, snapshot=None, station=None):
    """
    Phase E.2–E.3
    Read-only exposure of tool availability.
    Kernel remains authoritative.
    """

    tools = []

    # Resolve authoritative mode (edit / review / read-only)
    mode = resolve_mode(
        snapshot=snapshot,
        user=user,
        station=station,
    )

    for tool in get_all_tools():
        # 🔒 Phase E.3 — completed snapshots are immutable
        if snapshot and snapshot.status == "completed":
            tools.append(
                {
                    "tool_id": tool.name,
                    "availability": "blocked",
                    "reason": {
                        "code": "SNAPSHOT_FINALIZED",
                        "message": "Snapshot is finalized and read-only",
                    },
                }
            )
            continue

        # 🔒 Station mismatch
        if station and tool.required_station != station:
            tools.append(
                {
                    "tool_id": tool.name,
                    "availability": "blocked",
                    "reason": {
                        "code": "STATION_MISMATCH",
                        "message": "Tool not available in current station",
                    },
                }
            )
            continue

        # 🔒 Snapshot status mismatch
        if snapshot and snapshot.status not in tool.allowed_snapshot_statuses:
            tools.append(
                {
                    "tool_id": tool.name,
                    "availability": "blocked",
                    "reason": {
                        "code": "SNAPSHOT_STATE_MISMATCH",
                        "message": "Tool not available for current snapshot state",
                    },
                }
            )
            continue

        tools.append(
            {
                "tool_id": tool.name,
                "availability": "allowed",
                "reason": None,
            }
        )

    return {"tools": tools}

