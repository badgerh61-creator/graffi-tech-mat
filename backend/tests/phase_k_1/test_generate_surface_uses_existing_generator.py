from app.services import generate_surfaces_for_snapshot

def test_generate_surface_uses_existing_generator(
    db,
    solved_draft_snapshot,
    editor_user,
):
    new_snapshot = generate_surfaces_for_snapshot(
        db=db,
        snapshot=solved_draft_snapshot,
        user=editor_user,
    )

    assert len(new_snapshot.surfaces) == 1
    surface = new_snapshot.surfaces[0]
    assert surface.method == "loft"

