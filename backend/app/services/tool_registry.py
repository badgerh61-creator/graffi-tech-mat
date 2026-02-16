# backend/app/services/tool_registry.py

"""
Phase T — Tool Registry

Authoritative registry for studio tools.
Tools adapt to existing execution primitives.
"""

from fastapi import HTTPException

from app.services.transform_executor import apply_transform

# ✅ NEW: tuning executors
from app.services.tuning_mutation import (
    update_engine_config,
    update_suspension_config,
)


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
}


def get_tool(tool_name: str) -> Tool:
    tool = TOOLS.get(tool_name)
    if not tool:
        raise HTTPException(422, f"Unknown tool: {tool_name}")
    return tool

