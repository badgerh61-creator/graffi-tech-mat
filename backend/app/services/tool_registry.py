# backend/app/services/tool_registry.py

"""
Phase T — Tool Registry

Authoritative registry for studio tools.
Tools adapt to existing execution primitives.
"""

from fastapi import HTTPException

from app.services.transform_executor import apply_transform


class Tool:
    def __init__(self, *, name, is_mutating: bool):
        self.name = name
        self.is_mutating = is_mutating

    def execute(self, *, db, snapshot, user, params):
        """
        All tools adapt to the canonical transform executor.
        """
        return apply_transform(
            db=db,
            snapshot=snapshot,
            user=user,
            operation=self.name,
            target_id=params.get("target_id", "default"),
            params=params,
        )


TOOLS = {
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
}


def get_tool(tool_name: str) -> Tool:
    tool = TOOLS.get(tool_name)
    if not tool:
        raise HTTPException(422, f"Unknown tool: {tool_name}")
    return tool

