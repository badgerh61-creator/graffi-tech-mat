def test_multiple_read_views_allowed(
    db,
    draft_snapshot,
    viewer_user,
    editor_user,
    start_session_fn,
    open_read_view_fn,
):
    start_session_fn(db=db, user=viewer_user, project_id=draft_snapshot.project_id)
    start_session_fn(db=db, user=editor_user, project_id=draft_snapshot.project_id)

    view_a = open_read_view_fn(db=db, snapshot=draft_snapshot, user=viewer_user)
    view_b = open_read_view_fn(db=db, snapshot=draft_snapshot, user=editor_user)

    assert view_a.snapshot_id == draft_snapshot.id
    assert view_b.snapshot_id == draft_snapshot.id

