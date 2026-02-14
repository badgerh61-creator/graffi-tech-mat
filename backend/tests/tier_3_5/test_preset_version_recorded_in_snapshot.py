from app.services.decor_application import apply_decor_preset


def test_preset_version_recorded_in_snapshot(
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

    assert new_snapshot.applied_presets[0]["preset_id"] == decor_preset["name"]
    assert new_snapshot.applied_presets[0]["preset_version"] == decor_preset["version"]

