def test_set_material_invalid_panel(
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
            "panel": "non_existent_panel",
            "material": {
                "material_id": "mat_1",
                "parameters": {
                    "color": "#00FF00",
                    "finish": "matte",
                },
            },
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 400
    assert response.json()["error"] == "invalid_target_panel"

