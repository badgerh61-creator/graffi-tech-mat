def test_ai_never_mutates_geometry(
    db,
    assistant_service,
    editor_user,
    snapshot,
):
    before_hash = snapshot.scene_state_hash

    assistant_service.handle_request(
        user=editor_user,
        snapshot=snapshot,
        mode="proposal",
        prompt="Optimize shape",
    )

    db.refresh(snapshot)
    assert snapshot.scene_state_hash == before_hash
