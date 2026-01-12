def test_set_suspension_invalid_snapshot_base(
    client,
    project,
    failed_snapshot,
    editor_user,
):
    response = client.post(
        "/mutations/tuning/set-suspension",
        json={
            "project_id": project.id,
            "snapshot_base_id": failed_snapshot.id,
            "preset_id": "sport_low",
        },
        headers=auth(editor_user),
    )

    assert response.status_code == 409
    assert response.json()["error"] == "invalid_snapshot_base"

