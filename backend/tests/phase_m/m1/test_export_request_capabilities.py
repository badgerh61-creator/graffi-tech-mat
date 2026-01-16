def test_viewer_cannot_request_export(
    client,
    project,
    completed_snapshot,
    viewer_user,
):
    response = client.post(
        "/exports/requests",
        json={
            "project_id": project.id,
            "snapshot_id": completed_snapshot.id,
            "export_type": "image",
            "options": {},
        },
        headers=auth(viewer_user),
    )

    assert response.status_code == 403

