from fastapi import HTTPException
from app.studio.flow_graph import FLOW_GRAPH

def require_flow_allowed(*, current_state, next_tool):
    allowed = FLOW_GRAPH.get(current_state, set())

    if next_tool not in allowed:
        raise HTTPException(
            status_code=409,
            detail=f"Illegal flow transition: {current_state} → {next_tool}",
        )

def enforce_flow_transition(*, db, user, snapshot, next_state):
    require_active_session(db=db, user=user, project_id=snapshot.project_id)

    if snapshot.status != "draft" and next_state.requires_draft:
        raise HTTPException(409, "Invalid flow transition")

