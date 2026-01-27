from fastapi import HTTPException
from app.studio.tool_registry import get_tool

def require_tool_allowed(*, tool_name, snapshot, station, capabilities):
    tool = get_tool(tool_name)

    if not tool:
        raise HTTPException(404, "Tool not registered")

    if snapshot.status not in tool.allowed_snapshot_statuses:
        raise HTTPException(409, "Tool not allowed on snapshot state")

    if station != tool.required_station:
        raise HTTPException(409, "Tool not allowed in current station")

    if not capabilities.get(tool.required_capability, False):
        raise HTTPException(403, "Missing required capability")

    return tool

