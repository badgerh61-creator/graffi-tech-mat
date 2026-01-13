def test_brakes_deterministic(client, admin_user, completed_snapshot):
    auth(admin_user)

    r1 = client.post("/mutations/tuning/set-brakes", json={
        "project_id": completed_snapshot.project_id,
        "snapshot_base_id": completed_snapshot.id,
        "preset_id": "sport",
    })

    r2 = client.post("/mutations/tuning/set-brakes", json={
        "project_id": completed_snapshot.project_id,
        "snapshot_base_id": completed_snapshot.id,
        "preset_id": "sport",
    })

    assert r1.json()["snapshot_id"] == r2.json()["snapshot_id"]

