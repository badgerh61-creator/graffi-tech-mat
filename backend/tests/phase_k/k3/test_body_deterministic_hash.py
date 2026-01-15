def test_body_deterministic_hash(
    client,
    completed_snapshot,
    admin_user,
):
    payload = {
        "project_id": completed_snapshot.project_id,
        "base_snapshot_id": completed_snapshot.id,
        "preset_id": "widebody_v1",
        "parameters": {},
    }

    r1 = client.post("/mutations/body/apply-morph", json=payload)
    r2 = client.post("/mutations/body/apply-morph", json=payload)

    assert r1.json()["hash"] == r2.json()["hash"]

