from app.services.constraint_validator import validate_transform
from app.services.command_graph import create_command

def execute_transform(
    *,
    db,
    snapshot,
    target_id: str,
    operation: str,
    params: dict,
    constraints: list,
    user,
):
    # Phase 5.4 — immutable snapshots
    if snapshot.status != "draft":
        return {
            "applied": False,
            "violations": ["snapshot_not_draft"],
        }

    violations = validate_transform(
        snapshot=snapshot,
        target=target_id,
        operation=operation,
        params=params,
        constraints=constraints,
    )

    if violations:
        return {
            "applied": False,
            "violations": violations,
        }

    snapshot.apply_transform(
        target_id=target_id,
        operation=operation,
        params=params,
    )

    command = create_command(
        db=db,
        snapshot=snapshot,
        operation=operation,
        target_id=target_id,
        params=params,
        user=user,
    )

    db.commit()

    return {
        "applied": True,
        "command_id": command.id,
    }

