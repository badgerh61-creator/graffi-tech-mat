def test_viewer_cannot_set_material(
    client,
    project,
    completed_snapshot,
    viewer_user,
):
    response = client.post(
        "/mutations/decor/exterior/set-material",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "panel": "door_left",
            "material": {
                "material_id": "mat_1",
                "parameters": {
                    "color": "#FF0000",
                    "finish": "gloss",
                },
            },
        },
        headers=auth(viewer_user),
    )

    assert response.status_code == 403
    assert response.json()["error"] == "decor_capability_required"

