def test_engine_tune_creates_new_snapshot(
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
            "preset_id": "sport",
        },
    )

    assert response.status_code == 200
    assert response.json()["snapshot_id"] != completed_snapshot.id

