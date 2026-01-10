def test_set_material_invalid_material(
    client,
    project,
    completed_snapshot,
    editor_user,
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
                    "color": "red",
                    "finish": "unknown",
                },
            },
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 400
    assert response.json()["error"] == "invalid_material_definition"

