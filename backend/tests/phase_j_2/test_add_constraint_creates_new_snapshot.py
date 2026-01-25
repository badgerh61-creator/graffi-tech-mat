from app.services.curve_constraints import add_curve_constraint

def test_add_constraint_creates_new_snapshot(
    db,
    draft_snapshot,
    curve,
    editor_user,
):
    new_snapshot, constraint = add_curve_constraint(
        db=db,
        snapshot=draft_snapshot,
        curve=curve,
        user=editor_user,
        constraint_type="horizontal",
        reference="x-axis",
        params={},
    )

    assert new_snapshot.id != draft_snapshot.id
    assert new_snapshot.parent_snapshot_id == draft_snapshot.id
    assert constraint.id is not None

