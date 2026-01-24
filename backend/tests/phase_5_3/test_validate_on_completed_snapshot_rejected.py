def test_validate_on_completed_snapshot_rejected(
    client,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        f"/projects/{completed_snapshot.project_id}/snapshots/{completed_snapshot.id}/validate-transform",
        json={},
        headers=auth(editor_user),
    )

    assert response.status_code == 409

