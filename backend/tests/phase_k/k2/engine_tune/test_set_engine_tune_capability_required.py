def test_engine_tune_requires_can_tune(
    client,
    editor_user_without_tuning_capability,
    completed_snapshot,
):
    auth(editor_user_without_tuning_capability)

    response = client.post(
        "/mutations/tuning/set-engine-tune",
        json={
            "project_id": completed_snapshot.project_id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport",
        },
    )

    assert response.status_code == 403

