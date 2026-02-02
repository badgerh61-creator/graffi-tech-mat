def test_snapshot_never_mutated_under_stress(
    db,
    completed_snapshot,
    editor_user,
):
    original_hash = completed_snapshot.scene_state_hash

    for _ in range(10):
        try:
            execute_tool(
                db=db,
                user=editor_user,
                snapshot=completed_snapshot,
                tool="translate",
                params={"x": 1},
            )
        except:
            pass

    assert completed_snapshot.scene_state_hash == original_hash

