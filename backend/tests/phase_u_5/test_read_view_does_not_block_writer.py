def test_read_view_does_not_block_writer(
    db,
    draft_snapshot,
    owner_user,
    viewer_user,
    start_session_fn,
    acquire_draft_lock_fn,
    open_read_view_fn,
    execute_tool_fn,
):
    start_session_fn(db=db, user=owner_user, project_id=draft_snapshot.project_id)
    start_session_fn(db=db, user=viewer_user, project_id=draft_snapshot.project_id)

    acquire_draft_lock_fn(
        db=db,
        snapshot=draft_snapshot,
        user=owner_user,
    )

    open_read_view_fn(
        db=db,
        snapshot=draft_snapshot,
        user=viewer_user,
    )

    new_snapshot = execute_tool_fn(
        db=db,
        user=owner_user,
        snapshot=draft_snapshot,
        tool="translate",
        params={"x": 1},
    )

    assert new_snapshot.parent_snapshot_id == draft_snapshot.id

