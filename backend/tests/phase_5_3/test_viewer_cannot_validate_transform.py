def test_viewer_cannot_validate_transform(
    client,
    draft_snapshot,
    viewer_user,
):
    response = client.post(
        f"/projects/{draft_snapshot.project_id}/snapshots/{draft_snapshot.id}/validate-transform",
        json={},
        headers=auth(viewer_user),
    )

    assert response.status_code == 403

