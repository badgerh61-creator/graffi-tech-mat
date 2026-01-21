def test_finalize_draft_snapshot_success(
    client,
    draft_snapshot,
    editor_user,
):
    response = client.post(
        f"/projects/{draft_snapshot.project_id}/snapshots/{draft_snapshot.id}/finalize",
        headers=auth(editor_user),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"

