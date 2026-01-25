from app.services.constraint_solver import solve_constraints

def test_solve_constraints_success(
    db,
    constrained_draft_snapshot,
    editor_user,
):
    solved = solve_constraints(
        db=db,
        snapshot=constrained_draft_snapshot,
        user=editor_user,
    )

    assert solved.id != constrained_draft_snapshot.id
    assert solved.parent_snapshot_id == constrained_draft_snapshot.id
    assert solved.status == "draft"

