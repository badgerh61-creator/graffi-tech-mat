def test_invalid_brake_preset(client, admin_user, completed_snapshot):
    auth(admin_user)

    res = client.post(
        "/mutations/tuning/set-brakes",
        json={
            "project_id": completed_snapshot.project_id,
            "snapshot_base_id": completed_snapshot.id,
            "preset_id": "not-real",
        },
    )

    assert res.status_code == 404

