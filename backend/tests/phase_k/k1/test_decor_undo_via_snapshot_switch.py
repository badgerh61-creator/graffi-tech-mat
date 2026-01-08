def test_decor_undo_uses_snapshot_switch(
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

    new_snapshot_id = response.json()["snapshot_id"]

    switch = client.post(
        f"/projects/{project.id}/snapshots/active",
        json={"snapshot_id": completed_snapshot.id},
        headers=auth(editor_user),
    )

    assert switch.status_code == 200

