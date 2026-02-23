from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.tools import ToolExecuteRequest, ToolExecuteResponse

router = APIRouter(prefix="/tools", tags=["tools"])


@router.post("/execute", response_model=ToolExecuteResponse)
def execute_tool(
    body: ToolExecuteRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        from app.models.rendered_snapshot import RenderedSnapshot as Snapshot
    except Exception:
        from app.models.snapshot import Snapshot  # type: ignore

    snapshot = db.query(Snapshot).filter(Snapshot.id == body.snapshot_id).first()
    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    # Phase T optional governance (if your evaluator exists)
    try:
        from app.services.studio_kernel_executor import evaluate_tool_invocation

        decision = evaluate_tool_invocation(
            user=user,
            snapshot=snapshot,
            station=body.station,
            tool=body.tool,
            payload={"target_id": body.payload.target_id, "params": body.payload.params},
        )
        if not getattr(decision, "allowed", False):
            raise HTTPException(409, getattr(decision, "reason", "Tool rejected"))
    except HTTPException:
        raise
    except Exception:
        pass

    from app.services.transform_tool_service import execute_transform_tool

    new_snapshot = execute_transform_tool(
        db=db,
        snapshot=snapshot,
        user=user,
        station=body.station,
        tool=body.tool,
        payload={"target_id": body.payload.target_id, "params": body.payload.params},
    )

    return ToolExecuteResponse(new_snapshot_id=new_snapshot.id)
