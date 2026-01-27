from fastapi import HTTPException
from app.studio.flow_graph import FLOW_GRAPH

def require_flow_allowed(*, current_state, next_tool):
    allowed = FLOW_GRAPH.get(current_state, set())

    if next_tool not in allowed:
        raise HTTPException(
            status_code=409,
            detail=f"Illegal flow transition: {current_state} → {next_tool}",
        )

