def test_viewer_cannot_set_wheels(
    client,
    project,
    completed_snapshot,
    viewer_user,
):
    response = client.post(
        "/mutations/tuning/set-wheels",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "diameter": 19,
            "width": 9.5,
            "offset": 35,
        },
        headers=auth(viewer_user),
    )

    assert response.status_code == 403
    assert response.json()["error"] == "tuning_capability_required"

