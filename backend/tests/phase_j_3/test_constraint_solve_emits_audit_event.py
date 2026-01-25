from app.services.constraint_solver import solve_constraints
from app.models.audit_log import AuditLog

def test_constraint_solve_emits_audit_event(
    db,
    constrained_draft_snapshot,
    editor_user,
):
    solved = solve_constraints(
        db=db,
        snapshot=constrained_draft_snapshot,
        user=editor_user,
    )

    events = db.query(AuditLog).filter(
        AuditLog.action == "curve.constraints.solved",
        AuditLog.resource_id == solved.id,
    ).all()

    assert len(events) == 1

