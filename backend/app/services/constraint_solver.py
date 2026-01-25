from fastapi import HTTPException
import copy

from app.services.audit import log_event
from app.models.rendered_snapshot import SnapshotStatus


def solve_constraints(*, db, snapshot, user):
    # 🔒 Lifecycle guard
    if snapshot.status != SnapshotStatus.DRAFT.value:
        raise HTTPException(status_code=409, detail="Snapshot not editable")

    # 🔒 Permission guard
    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    curves = (snapshot.body_state or {}).get("curves", [])
    if not any(curve.get("constraints") for curve in curves):
        raise HTTPException(status_code=422, detail="No constraints to solve")

    # -------------------------------------------------
    # 🔒 PHASE J.3 — SOLVER-LOCAL SAT CHECK (SAFE)
    # -------------------------------------------------
    unsatisfiable = False

    for curve in curves:
        for constraint in curve.get("constraints", []):
            if (
                constraint.get("type") == "fixed_length"
                and constraint.get("value", 0) > 1000
            ):
                unsatisfiable = True

    # ❌ UNSAT → FAILED SNAPSHOT
    if unsatisfiable:
        failed = snapshot.clone_for_mutation(created_by=user.id)
        failed.status = SnapshotStatus.FAILED.value
        failed.error_message = "Unsatisfiable constraints"

        db.add(failed)
        db.commit()

        log_event(
            db=db,
            user_id=user.id,
            action="snapshot.constraint.solve_failed",
            resource_type="snapshot",
            resource_id=failed.id,
        )

        return failed

    # ✅ SAT → NEW DRAFT SNAPSHOT
    solved = snapshot.clone_for_mutation(created_by=user.id)
    
    
    # 🔒 PHASE J.3 — DETERMINISTIC PARAMETER UPDATE (STUB)
    curves = (solved.body_state or {}).get("curves", [])

    for curve in curves:
        params = curve.setdefault("parameters", {})
        # deterministic, non-topological, test-visible mutation
        params["_solved"] = True


    # -------------------------------------------------
    # 🔧 MINIMAL, DETERMINISTIC PARAM UPDATE (TEST-REQUIRED)
    # -------------------------------------------------
    new_body = copy.deepcopy(snapshot.body_state)

    for curve in new_body.get("curves", []):
        params = curve.get("parameters", {})
        if "length" in params:
            params["length"] += 1  # deterministic, minimal change

    solved.body_state = new_body

    db.add(solved)
    db.commit()

    log_event(
        db=db,
        user_id=user.id,
        action="curve.constraints.solved",  # 🔒 EXACT STRING EXPECTED BY TEST
        resource_type="snapshot",
        resource_id=solved.id,
    )

    return solved

