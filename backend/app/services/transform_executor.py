from fastapi import HTTPException
from datetime import datetime

from app.services.presence_sessions import require_active_session
from app.services.constraint_validator import validate_transform
from app.services.command_graph import create_command
from app.models.snapshot import Snapshot


ALLOWED_OPERATIONS = {"translate", "rotate", "scale"}


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
    """
    Phase 5.4 + Phase U.1
    Constraint-aware, immutable transform execution.
    """

    # 🔒 Phase U.1 — session authority
    require_active_session(
        db=db,
        user=user,
        project_id=snapshot.project_id,
        snapshot_id=snapshot.id,
    )

    # 🔒 Phase 5 — lifecycle enforcement
    if snapshot.status != "draft":
        raise HTTPException(409, "Only draft snapshots may be transformed")

    # 🔒 Operation validation
    if operation not in ALLOWED_OPERATIONS:
        raise HTTPException(422, "Invalid transform operation")

    # 🔒 Constraint validation (pure)
    violations = validate_transform(
        snapshot=snapshot,
        target=target_id,
        operation=operation,
        params=params,
        constraints=constraints,
    )

    if violations:
        raise HTTPException(
            status_code=409,
            detail={
                "reason": "constraint_violation",
                "violations": violations,
            },
        )

    # 🧱 Phase 5.4 — create new draft snapshot (no mutation)
    new_snapshot = Snapshot(
        project_id=snapshot.project_id,
        parent_snapshot_id=snapshot.id,

        # 🔒 Phase 5 invariants — MUST be copied
        scene_state_hash=snapshot.scene_state_hash,
        render_profile=snapshot.render_profile,
        engine_version=snapshot.engine_version,
        deterministic_key=snapshot.deterministic_key,

        status="draft",
        created_by=user.id,
        created_at=datetime.utcnow(),
    )

    db.add(new_snapshot)
    db.flush()  # obtain ID before command creation

    # 🧠 Command graph (authoritative history)
    create_command(
        db=db,
        snapshot=new_snapshot,
        operation=operation,
        target_id=target_id,
        params=params,
        user=user,
    )

    db.commit()
    db.refresh(new_snapshot)

    # 🔁 Return the new snapshot (history is the truth)
    return new_snapshot


# Phase U compatibility alias
def apply_transform(*, db, snapshot, user, operation, target_id, params, constraints=None):
    return execute_transform(
        db=db,
        snapshot=snapshot,
        user=user,
        operation=operation,
        target_id=target_id,
        params=params,
        constraints=constraints or [],
    )
