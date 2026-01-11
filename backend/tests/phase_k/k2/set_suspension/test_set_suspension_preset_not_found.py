def test_set_suspension_preset_not_found(
    client,
    project,
    completed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/tuning/set-suspension",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "non_existent_preset",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 404
    assert response.json()["error"] == "suspension_preset_not_found"

