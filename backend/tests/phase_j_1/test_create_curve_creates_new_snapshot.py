from app.services.curve_creator import create_curve

def test_create_curve_creates_new_snapshot(
    db,
    draft_snapshot,
    editor_user,
):
    new_snapshot, curve = create_curve(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
        curve_type="line",
        reference_plane_id="front",
        params={"x1": 0, "y1": 0, "x2": 100, "y2": 0},
        constraints=["horizontal"],
    )

    assert new_snapshot.id != draft_snapshot.id
    assert new_snapshot.parent_snapshot_id == draft_snapshot.id
    assert curve.id is not None

