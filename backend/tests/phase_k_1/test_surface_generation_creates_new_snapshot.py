from app.services import generate_surfaces_for_snapshot

def test_surface_generation_creates_new_snapshot(
    db,
    solved_draft_snapshot,
    editor_user,
):
    new_snapshot = generate_surfaces_for_snapshot(
        db=db,
        snapshot=solved_draft_snapshot,
        user=editor_user,
    )

    assert new_snapshot.id != solved_draft_snapshot.id
    assert new_snapshot.parent_snapshot_id == solved_draft_snapshot.id

