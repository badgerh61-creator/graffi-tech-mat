def test_editor_without_tuning_capability_cannot_set_wheels(
    client,
    project,
    completed_snapshot,
    editor_user_without_tuning_capability,
):
    response = client.post(
        "/mutations/tuning/set-wheels",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "diameter": 18,
            "width": 8,
            "offset": 40,
        },
        headers=auth(editor_user_without_tuning_capability),
    )

    assert response.status_code == 403
    assert response.json()["error"] == "tuning_capability_required"

