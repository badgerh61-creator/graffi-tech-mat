from app.services.constraint_solver import solve_constraints

def test_curve_parameters_updated_on_solve(
    db,
    constrained_draft_snapshot,
    editor_user,
):
    solved = solve_constraints(
        db=db,
        snapshot=constrained_draft_snapshot,
        user=editor_user,
    )

    solved_curve = solved.curves[0]
    original_curve = constrained_draft_snapshot.curves[0]

    assert solved_curve.parameters != original_curve.parameters

