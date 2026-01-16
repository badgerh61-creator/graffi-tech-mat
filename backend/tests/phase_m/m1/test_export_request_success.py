def test_export_request_image_success(
    client,
    project,
    completed_snapshot,
    owner_user,
):
    response = client.post(
        "/exports/requests",
        json={
            "project_id": project.id,
            "snapshot_id": completed_snapshot.id,
            "export_type": "image",
            "options": {
                "format": "png",
                "resolution": {"width": 2048, "height": 2048}
            },
        },
        headers=auth(owner_user),
    )

    assert response.status_code == 200

    data = response.json()
    assert "export_request_id" in data
    assert data["status"] == "accepted"

