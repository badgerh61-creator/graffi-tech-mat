def test_invalid_snapshot_rejected(client, admin_user, pending_snapshot):
    auth(admin_user)

    res = client.post(
        "/mutations/tuning/set-brakes",
        json={
            "project_id": pending_snapshot.project_id,
            "snapshot_base_id": pending_snapshot.id,
            "preset_id": "sport",
        },
    )

    assert res.status_code == 409

