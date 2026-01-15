def test_invalid_snapshot_base(client, obsolete_snapshot, admin_user):
    payload = {
        "project_id": obsolete_snapshot.project_id,
        "base_snapshot_id": obsolete_snapshot.id,
        "preset_id": "widebody_v1",
        "parameters": {},
    }

    res = client.post("/mutations/body/apply-morph", json=payload)
    assert res.status_code == 409

