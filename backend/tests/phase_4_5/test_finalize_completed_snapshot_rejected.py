def test_finalize_completed_snapshot_rejected(
    client,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        f"/projects/{completed_snapshot.project_id}/snapshots/{completed_snapshot.id}/finalize",
        headers=auth(editor_user),
    )

    assert response.status_code == 409

