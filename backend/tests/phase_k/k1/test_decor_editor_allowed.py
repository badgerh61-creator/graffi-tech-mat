def test_editor_can_apply_decal(
    client,
    project,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/decor/exterior/apply-decal",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "decal_id": "test_decal",
            "target": {
                "panel": "door_left",
                "uv_transform": {
                    "x": 0.1,
                    "y": 0.2,
                    "scale": 1.0,
                    "rotation": 0
                }
            }
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 200
    assert "snapshot_id" in response.json()

