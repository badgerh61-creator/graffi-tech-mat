def test_batch_status_endpoint(client, draft_snapshot, viewer_user):
    r1 = client.post(
        "/simulation/batches",
        json={"snapshot_id": draft_snapshot.id, "template_keys": ["accel_0_60_v1"]},
        headers=auth(viewer_user),
    )
    assert r1.status_code == 200
    batch_id = r1.json()["batch_id"]

    r2 = client.get(f"/simulation/batches/{batch_id}", headers=auth(viewer_user))
    assert r2.status_code == 200
    st = r2.json()
    assert st["batch_id"] == batch_id
    assert st["snapshot_id"] == draft_snapshot.id
