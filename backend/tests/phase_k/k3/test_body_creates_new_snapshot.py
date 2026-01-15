def test_body_creates_new_snapshot(
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

    res = client.post("/mutations/body/apply-morph", json=payload)

    assert res.status_code == 200
    assert res.json()["snapshot_id"] != completed_snapshot.id
