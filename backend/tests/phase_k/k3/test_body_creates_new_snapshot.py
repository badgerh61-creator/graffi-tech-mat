def test_body_creates_new_snapshot(client, admin_user, snapshot):
    res = client.post("/mutations/body/apply-morph", json={
        "project_id": snapshot.project_id,
        "base_snapshot_id": snapshot.id,
        "preset_id": "widebody_v1",
        "parameters": {}
    }, user=admin_user)

    assert res.json()["snapshot_id"] != snapshot.id

