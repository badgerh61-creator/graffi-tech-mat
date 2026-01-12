def test_set_suspension_requires_capability(
    client,
    project,
    completed_snapshot,
    editor_user_without_tune_cap,
):
    response = client.post(
        "/mutations/tuning/set-suspension",
        json={
            "project_id": project.id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport_low",
        },
        headers=auth(editor_user_without_tune_cap),
    )

    assert response.status_code == 403
    assert response.json()["error"] == "tuning_capability_required"

