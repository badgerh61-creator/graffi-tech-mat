def test_decor_does_not_mutate_base_snapshot(
    client,
    db,
    project,
    completed_snapshot,
    editor_user,
):
    original_hash = completed_snapshot.hash

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

    db.refresh(completed_snapshot)
    assert completed_snapshot.hash == original_hash

