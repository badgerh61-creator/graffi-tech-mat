# backend/app/services/tool_registry.py

"""
Phase T — Tool Registry

Authoritative registry for studio tools.
Tools adapt to existing execution primitives.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.transform_executor import apply_transform

# ✅ NEW: tuning executors
from app.services.tuning_mutation import (
    update_engine_config,
    update_suspension_config,
)

# ✅ Tier 7.33: parametric components (executor helpers)
from app.services.components.store import find_component, upsert_component
from app.services.components.compiler import compile_component_ops

# ✅ Tier 7.46: scene objects mutations
from app.services.mutations.scene_objects import (
    validate_add_model_ref,
    validate_remove_object,
    apply_add_model_ref,
    apply_remove_object,
)

# ✅ Tier 7.46: asset permission check reuse (same as api/assets.py)
from app.models.asset import Asset
from app.models.model import ModelRecord
from app import crud


class Tool:
    def __init__(self, *, name, is_mutating: bool, executor=None):
        self.name = name
        self.is_mutating = is_mutating
        self.executor = executor  # ✅ optional custom executor

    def execute(self, *, db, snapshot, user, params):
        """
        Default behavior: transform executor.
        Extended behavior: custom executor if provided.
        """

        # ✅ Custom executor support (NON-BREAKING)
        if self.executor:
            return self.executor(
                db=db,
                snapshot=snapshot,
                user=user,
                params=params,
            )

        # 🔒 Existing behavior preserved
        return apply_transform(
            db=db,
            snapshot=snapshot,
            user=user,
            operation=self.name,
            target_id=params.get("target_id", "default"),
            params=params,
        )


# ✅ Tier 7.33: leaf tool executor (returns a NEW snapshot, like other tools)
def _execute_apply_component(*, db, snapshot, user, params):
    component_id = str((params or {}).get("component_id") or "")
    if not component_id:
        raise HTTPException(422, "component_id required")

    current = find_component(snapshot, component_id)
    if not current:
        raise HTTPException(409, "component not found")

    next_params = (params or {}).get("next_params") or {}
    target_id = (params or {}).get("target_id") or current.get("target_id")

    kind = current.get("kind") or "custom"
    ops = compile_component_ops(kind=kind, params=next_params, target_id=target_id)

    # 1) Create a new snapshot first so component params persist even if ops is empty
    new_snapshot = snapshot.clone_for_mutation(
        created_by=user.id,
    )
    db.add(new_snapshot)
    db.commit()

    # 2) Persist component state onto the new snapshot
    next_component = {
        **current,
        "params": next_params,
        "target_id": target_id,
        "version": int(current.get("version") or 1),
        "enabled": bool(current.get("enabled", True)),
    }
    upsert_component(new_snapshot, next_component)

    # 3) Execute compiled ops sequentially (each op returns a new snapshot)
    working = new_snapshot
    for op in ops:
        op_tool = op.get("tool")
        op_payload = op.get("payload") or {}
        if not op_tool:
            continue

        # Compiler emits "TRANSLATE"/"ROTATE"/"SCALE" — registry uses "translate"/"rotate"/"scale"
        leaf = (
            str(op_tool).lower()
            if str(op_tool).upper() in ("TRANSLATE", "ROTATE", "SCALE")
            else str(op_tool)
        )

        working = apply_transform(
            db=db,
            snapshot=working,
            user=user,
            operation=leaf,
            target_id=op_payload.get("target_id", "default"),
            params=op_payload,
        )

    return working


# ✅ Tier 7.46: helper to enforce asset access (same access model as api/assets.py)
def _require_asset_access(*, db: Session, user_id: int, asset_id: int) -> None:
    asset = (
        db.query(Asset)
        .join(ModelRecord)
        .filter(Asset.id == asset_id)
        .first()
    )
    if not asset:
        raise HTTPException(404, "Asset not found")

    model = crud.get_model_if_accessible(db, model_id=asset.model_id, user_id=user_id)
    if not model:
        raise HTTPException(403, "No access to asset")


# ✅ Tier 7.46: leaf tool executor — adds a model_ref object into snapshot.body_state.objects
def _execute_scene_add_model_ref(*, db, snapshot, user, params):
    err = validate_add_model_ref(params or {})
    if err:
        raise HTTPException(422, err)

    asset_id = int((params or {}).get("asset_id"))

    # permissions: reuse asset->model access check
    _require_asset_access(db=db, user_id=int(user.id), asset_id=asset_id)

    # create new snapshot and mutate it
    new_snapshot = snapshot.clone_for_mutation(created_by=user.id)
    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)

    apply_add_model_ref(new_snapshot, params or {})

    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)
    return new_snapshot


# ✅ Tier 7.46: leaf tool executor — removes an object from snapshot.body_state.objects
def _execute_scene_remove_object(*, db, snapshot, user, params):
    err = validate_remove_object(params or {})
    if err:
        raise HTTPException(422, err)

    new_snapshot = snapshot.clone_for_mutation(created_by=user.id)
    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)

    apply_remove_object(new_snapshot, params or {})

    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)
    return new_snapshot


TOOLS = {
    # --------------------------
    # Existing Phase Tools
    # --------------------------

    "scale": Tool(
        name="scale",
        is_mutating=True,
    ),
    "translate": Tool(
        name="translate",
        is_mutating=True,
    ),
    "rotate": Tool(
        name="rotate",
        is_mutating=True,
    ),

    # --------------------------
    # Tier 4.3 — Tuning Tools
    # --------------------------

    "UPDATE_ENGINE_CONFIG": Tool(
        name="UPDATE_ENGINE_CONFIG",
        is_mutating=True,
        executor=update_engine_config,  # ✅ custom
    ),

    "UPDATE_SUSPENSION_CONFIG": Tool(
        name="UPDATE_SUSPENSION_CONFIG",
        is_mutating=True,
        executor=update_suspension_config,  # ✅ custom
    ),

    # --------------------------
    # Tier 7.33 — Parametric Components
    # --------------------------

    "APPLY_COMPONENT": Tool(
        name="APPLY_COMPONENT",
        is_mutating=True,
        executor=_execute_apply_component,  # ✅ custom
    ),

    # --------------------------
    # Tier 7.46 — Scene Objects (Asset model refs)
    # --------------------------

    "SCENE_ADD_MODEL_REF": Tool(
        name="SCENE_ADD_MODEL_REF",
        is_mutating=True,
        executor=_execute_scene_add_model_ref,  # ✅ custom
    ),

    "SCENE_REMOVE_OBJECT": Tool(
        name="SCENE_REMOVE_OBJECT",
        is_mutating=True,
        executor=_execute_scene_remove_object,  # ✅ custom
    ),
}


def get_tool(tool_name: str) -> Tool:
    tool = TOOLS.get(tool_name)
    if not tool:
        raise HTTPException(422, f"Unknown tool: {tool_name}")
    return tool
