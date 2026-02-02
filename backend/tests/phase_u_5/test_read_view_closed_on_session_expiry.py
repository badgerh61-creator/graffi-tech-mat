def test_read_view_closed_on_session_expiry(
    db,
    draft_snapshot,
    viewer_user,
    start_session_fn,
    open_read_view_fn,
    has_active_read_view_fn,
    advance_time,
):
    start_session_fn(
        db=db,
        user=viewer_user,
        project_id=draft_snapshot.project_id,
        ttl_seconds=1,
    )

    open_read_view_fn(
        db=db,
        snapshot=draft_snapshot,
        user=viewer_user,
    )

   
    advance_time(seconds=2)

    assert not has_active_read_view_fn(
        db=db,
        snapshot=draft_snapshot,
        user=viewer_user,
    )

