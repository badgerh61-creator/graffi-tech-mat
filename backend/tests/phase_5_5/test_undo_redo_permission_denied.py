def test_undo_redo_permission_denied(
    client,
    transformed_snapshot,
    viewer_user,
):
    res = client.post(
        f"/projects/{transformed_snapshot.project_id}/snapshots/{transformed_snapshot.id}/undo",
        headers=auth(viewer_user),
    )

    assert res.status_code == 403

