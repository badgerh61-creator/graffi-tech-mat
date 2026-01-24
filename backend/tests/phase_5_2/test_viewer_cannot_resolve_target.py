def test_viewer_cannot_resolve_target(
    client,
    draft_snapshot,
    viewer_user,
):
    response = client.post(
        f"/projects/{draft_snapshot.project_id}/snapshots/{draft_snapshot.id}/resolve-target",
        json={
            "selection_type": "node",
            "selection_id": "body.root",
        },
        headers=auth(viewer_user),
    )

    assert response.status_code == 403

