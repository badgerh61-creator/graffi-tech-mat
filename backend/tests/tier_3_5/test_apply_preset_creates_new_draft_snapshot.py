from app.services.decor_application import apply_decor_preset


def test_apply_preset_creates_new_draft_snapshot(
    db,
    draft_snapshot,
    decor_preset,
    editor_user,
):
    new_snapshot = apply_decor_preset(
        db=db,
        snapshot=draft_snapshot,
        preset=decor_preset,
        user=editor_user,
    )

    assert new_snapshot.id != draft_snapshot.id
    assert new_snapshot.parent_snapshot_id == draft_snapshot.id
    assert new_snapshot.status == "draft"

