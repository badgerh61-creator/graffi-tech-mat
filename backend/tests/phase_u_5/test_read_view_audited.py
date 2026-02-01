def test_read_view_audited(
    db,
    draft_snapshot,
    viewer_user,
    start_session_fn,
    open_read_view_fn,
):
    start_session_fn(
        db=db,
        user=viewer_user,
        project_id=draft_snapshot.project_id,
    )

    open_read_view_fn(
        db=db,
        snapshot=draft_snapshot,
        user=viewer_user,
    )

