def test_engine_tune_invalid_snapshot(
    client,
    override_get_current_user,
    admin_user,
    obsolete_snapshot,
):
    response = client.post(
        "/mutations/tuning/set-engine-tune",
        json={
            "project_id": obsolete_snapshot.project_id,
            "snapshot_base_id": obsolete_snapshot.id,
            "preset_id": "sport",
        },
    )

    assert response.status_code == 409
    assert response.json()["error"] == "invalid_snapshot_base"

