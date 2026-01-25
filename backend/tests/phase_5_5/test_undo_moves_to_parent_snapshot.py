def test_undo_moves_to_parent_snapshot(
    client,
    transformed_snapshot,
    editor_user,
):
    res = client.post(
        f"/projects/{transformed_snapshot.project_id}/snapshots/{transformed_snapshot.id}/undo",
        headers=auth(editor_user),
    )

    data = res.json()
    assert data["active_snapshot_id"] == transformed_snapshot.parent_snapshot_id

