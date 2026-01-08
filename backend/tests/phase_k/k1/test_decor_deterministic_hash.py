def test_apply_decal_is_deterministic(
    client,
    project,
    completed_snapshot,
    editor_user,
):
    payload = {
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
    }

    first = client.post(
        "/mutations/decor/exterior/apply-decal",
        json=payload,
        headers=auth(editor_user),
    )

    second = client.post(
        "/mutations/decor/exterior/apply-decal",
        json=payload,
        headers=auth(editor_user),
    )

    assert first.json()["snapshot_id"] == second.json()["snapshot_id"]

