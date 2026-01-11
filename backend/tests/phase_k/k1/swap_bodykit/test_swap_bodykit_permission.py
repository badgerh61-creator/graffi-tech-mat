def test_viewer_cannot_swap_bodykit(
    client,
    project,
    completed_snapshot,
    viewer_user,
):
    response = client.post(
        "/mutations/decor/exterior/swap-bodykit",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "bodykit_id": "bk_1",
        },
        headers=auth(viewer_user),
    )

    assert response.status_code == 403
    assert response.json()["error"] == "decor_capability_required"

