def test_batch_create_validates_inputs(client, viewer_user):
    r = client.post("/simulation/batches", json={"snapshot_id": 1}, headers=auth(viewer_user))
    assert r.status_code == 422
