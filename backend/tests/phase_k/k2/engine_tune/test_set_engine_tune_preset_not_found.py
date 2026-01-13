def test_engine_tune_invalid_preset(
    client,
    override_get_current_user,
    admin_user,
    completed_snapshot,
):
    response = client.post(
        "/mutations/tuning/set-engine-tune",
        json={
            "project_id": completed_snapshot.project_id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "does_not_exist",
        },
    )

    assert response.status_code == 404
    assert response.json()["error"] == "engine_tune_preset_not_found"

