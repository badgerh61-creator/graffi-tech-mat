def test_redo_moves_to_child_snapshot(
    client,
    root_snapshot_with_child,
    editor_user,
):
    res = client.post(
        f"/projects/{root_snapshot_with_child.project_id}/snapshots/{root_snapshot_with_child.id}/redo",
        headers=auth(editor_user),
    )

    assert res.status_code == 200

    data = res.json()

    # Redo must move away from the root snapshot
    assert data["active_snapshot_id"] != root_snapshot_with_child.id


