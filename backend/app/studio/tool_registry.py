# backend/app/studio/tool_registry.py

from app.studio.tools import ToolDefinition
from app.studio.stations import StudioStation

TOOL_REGISTRY = {
    "translate": ToolDefinition(
        name="translate",
        operation="transform.translate",
        required_station=StudioStation.geometry,
        allowed_snapshot_statuses={"draft"},
        required_capability="canEditGeometry",
    ),
    "rotate": ToolDefinition(
        name="rotate",
        operation="transform.rotate",
        required_station=StudioStation.geometry,
        allowed_snapshot_statuses={"draft"},
        required_capability="canEditGeometry",
    ),
    "scale": ToolDefinition(
        name="scale",
        operation="transform.scale",
        required_station=StudioStation.geometry,
        allowed_snapshot_statuses={"draft"},
        required_capability="canEditGeometry",
    ),
    "finalize_snapshot": ToolDefinition(
        name="finalize_snapshot",
        operation="snapshot.finalize",
        required_station=StudioStation.review,
        allowed_snapshot_statuses={"draft"},
        required_capability="canFinalizeSnapshot",
    ),
}

def get_tool(tool_name: str) -> ToolDefinition:
    return TOOL_REGISTRY.get(tool_name)

def get_all_tools() -> list[ToolDefinition]:
    """
    Phase T.2 — Authoritative enumeration of all studio tools.
    Read-only. No mutation.
    """
    return list(TOOL_REGISTRY.values())

