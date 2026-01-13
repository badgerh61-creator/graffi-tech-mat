def test_engine_tune_is_deterministic(
    client,
    override_get_current_user,
    admin_user,
    completed_snapshot,
):
    payload = {
        "project_id": completed_snapshot.project_id,
        "snapshot_base_id": completed_snapshot.id,
        "preset_id": "sport",
    }

    r1 = client.post("/mutations/tuning/set-engine-tune", json=payload)
    r2 = client.post("/mutations/tuning/set-engine-tune", json=payload)

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()["snapshot_id"] == r2.json()["snapshot_id"]

