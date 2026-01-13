def test_brakes_creates_new_snapshot(client, admin_user, completed_snapshot, db):
    auth(admin_user)

    res = client.post(
        "/mutations/tuning/set-brakes",
        json={
            "project_id": completed_snapshot.project_id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "sport",
        },
    )

    assert res.status_code == 200
    assert res.json()["snapshot_id"] != completed_snapshot.id

