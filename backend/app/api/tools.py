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
        from app.models.snapshot import Snapshot

    snapshot = db.query(Snapshot).filter(Snapshot.id == body.snapshot_id).first()
    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    tool = body.tool

    # -----------------------------
    # normalize payload
    # -----------------------------
    if isinstance(body.payload, dict):
        payload = dict(body.payload)
    elif hasattr(body.payload, "dict"):
        payload = body.payload.dict()
    else:
        payload = {}

    if "preset_id" in payload:
        payload["preset"] = payload["preset_id"]

    print("EXEC TOOL:", tool)
    print("PAYLOAD:", payload)

    # =========================================================
    # PAINT LIBRARY PRESET (FIXED)
    # =========================================================

    if tool == "PAINT_APPLY_LIBRARY_PRESET":
        try:
            from app.services.materials.paint_mutator import (
                apply_apply_library_preset,
            )

            apply_apply_library_preset(
                snapshot,
                payload,
            )

            db.add(snapshot)
            db.commit()
            db.refresh(snapshot)

            return ToolExecuteResponse(new_snapshot_id=snapshot.id)

        except Exception as e:
            print("PAINT LIBRARY ERROR:", str(e))
            raise HTTPException(500, str(e))

    # =========================================================
    # PAINT
    # =========================================================

    if tool.startswith("PAINT_"):
        from app.services.tools.paint_tools import apply_paint_tool

        apply_paint_tool(
            snapshot=snapshot,
            tool=tool,
            payload=payload,
        )

        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)

        return ToolExecuteResponse(new_snapshot_id=snapshot.id)

    # =========================================================
    # MATERIAL
    # =========================================================

    if tool.startswith("MATERIAL_"):
        from app.services.tools.material_tools import apply_material_tool

        apply_material_tool(
            snapshot=snapshot,
            tool=tool,
            payload=payload,
        )

        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)

        return ToolExecuteResponse(new_snapshot_id=snapshot.id)

    # =========================================================
    # DECAL
    # =========================================================

    if tool.startswith("DECAL_"):
        from app.services.tools.decal_tools import apply_decal_tool

        apply_decal_tool(
            snapshot=snapshot,
            tool=tool,
            payload=payload,
        )

        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)

        return ToolExecuteResponse(new_snapshot_id=snapshot.id)

    # =========================================================
    # SCENE
    # =========================================================

    if tool.startswith("SCENE_"):
        from app.services.tools.scene_tools import apply_scene_tool

        apply_scene_tool(
            snapshot=snapshot,
            tool=tool,
            payload=payload,
        )

        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)

        return ToolExecuteResponse(new_snapshot_id=snapshot.id)

    # =========================================================
    # VARIANT
    # =========================================================

    if tool.startswith("VARIANT_"):
        from app.services.tools.variant_tools import apply_variant_tool

        apply_variant_tool(
            snapshot=snapshot,
            tool=tool,
            payload=payload,
        )

        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)

        return ToolExecuteResponse(new_snapshot_id=snapshot.id)

    # =========================================================
    # FALLBACK
    # =========================================================

    from app.services.transform_tool_service import execute_transform_tool

    new_snapshot = execute_transform_tool(
        db=db,
        snapshot=snapshot,
        user=user,
        station=body.station,
        tool=tool,
        payload=payload,
    )

    return ToolExecuteResponse(new_snapshot_id=new_snapshot.id)
