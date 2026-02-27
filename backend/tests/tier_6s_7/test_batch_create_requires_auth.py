def test_batch_create_requires_auth(client, draft_snapshot):
    r = client.post("/simulation/batches", json={"snapshot_id": draft_snapshot.id, "template_keys": ["accel_0_60_v1"]})
    assert r.status_code in (401, 403)
