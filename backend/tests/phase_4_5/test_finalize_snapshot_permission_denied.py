def test_viewer_cannot_finalize_snapshot(
    client,
    draft_snapshot,
    viewer_user,
):
    response = client.post(
        f"/projects/{draft_snapshot.project_id}/snapshots/{draft_snapshot.id}/finalize",
        headers=auth(viewer_user),
    )

    assert response.status_code == 403

