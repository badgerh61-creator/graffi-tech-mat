def test_create_draft_from_completed_snapshot(
    client,
    completed_snapshot,
    editor_user,
):
    res = client.post(
        f"/snapshots/{completed_snapshot.id}/draft",
        headers=auth(editor_user),
    )

    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "draft"
    assert data["parent_snapshot_id"] == completed_snapshot.id

