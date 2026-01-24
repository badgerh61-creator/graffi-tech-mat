def test_viewer_cannot_transform(
    client,
    draft_snapshot,
    viewer_user,
):
    response = client.post(
        f"/projects/{draft_snapshot.project_id}/snapshots/{draft_snapshot.id}/transform",
        json={
            "operation": "scale",
            "target_id": "body.root",
            "params": {"x": 1.2},
        },
        headers=auth(viewer_user),
    )

    assert response.status_code == 403

