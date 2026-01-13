def test_set_suspension_requires_capability(
    client,
    project,
    completed_snapshot,
    editor_user_without_tuning_capability,
):
    response = client.post(
        "/mutations/tuning/set-suspension",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport_low",
        },
        headers=auth(editor_user_without_tuning_capability),
    )

    assert response.status_code == 403

    body = response.json()
    assert "tuning" in body["detail"].lower()

