def test_redo_blocked_without_child(
    client,
    latest_snapshot,
    editor_user,
):
    res = client.post(
        f"/projects/{latest_snapshot.project_id}/snapshots/{latest_snapshot.id}/redo",
        headers=auth(editor_user),
    )

    assert res.status_code == 409

