from app.services.constraint_solver import solve_constraints

def test_unsatisfiable_constraints_produce_failed_snapshot(
    db,
    conflicting_constraints_snapshot,
    editor_user,
):
    failed = solve_constraints(
        db=db,
        snapshot=conflicting_constraints_snapshot,
        user=editor_user,
    )

    assert failed.status == "failed"
    assert failed.parent_snapshot_id == conflicting_constraints_snapshot.id

