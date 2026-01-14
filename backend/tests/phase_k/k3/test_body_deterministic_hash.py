def test_body_deterministic_hash(client, admin_user, snapshot):
    payload = {
        "project_id": snapshot.project_id,
        "base_snapshot_id": snapshot.id,
        "preset_id": "widebody_v1",
        "parameters": {}
    }

    r1 = client.post("/mutations/body/apply-morph", json=payload, user=admin_user)
    r2 = client.post("/mutations/body/apply-morph", json=payload, user=admin_user)

    assert r1.json()["hash"] == r2.json()["hash"]

