from app.services.studio_kernel_guard import enforce_tool_authority
from app.services.read_view_guard import reject_mutation_from_read_view
from app.services.snapshot_mutations import apply_transform


class Tool:
    def __init__(self, *, name, is_mutating):
        self.name = name
        self.is_mutating = is_mutating

    def execute(self, *, db, snapshot, user, params):
        if self.name in ("translate", "scale", "rotate"):
            return apply_transform(
                db=db,
                snapshot=snapshot,
                user=user,
                operation=self.name,
                target_id=params.get("target_id", "default"),
                params=params,
            )
        raise ValueError(f"Unknown tool: {self.name}")


TOOL_REGISTRY = {
    "translate": Tool(name="translate", is_mutating=True),
    "scale": Tool(name="scale", is_mutating=True),
    "rotate": Tool(name="rotate", is_mutating=True),
}


def execute_tool(*, db, user, snapshot, tool, params):
    # 🔒 CRITICAL: sync snapshot ownership from DB
    db.refresh(snapshot)

    # 🔁 Resolve string → Tool (LOCAL, AUTHORITATIVE)
    tool_obj = TOOL_REGISTRY[tool] if isinstance(tool, str) else tool

    reject_mutation_from_read_view(
        db=db,
        snapshot=snapshot,
        user=user,
    )

    enforce_tool_authority(
        db=db,
        user=user,
        snapshot=snapshot,
        tool=tool_obj,
    )

    return tool_obj.execute(
        db=db,
        snapshot=snapshot,
        user=user,
        params=params,
    )

