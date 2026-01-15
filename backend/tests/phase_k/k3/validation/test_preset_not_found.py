def test_body_preset_not_found(client, completed_snapshot, admin_user):
    payload = {
        "project_id": completed_snapshot.project_id,
        "base_snapshot_id": completed_snapshot.id,
        "preset_id": "does_not_exist",
        "parameters": {},
    }

    res = client.post("/mutations/body/apply-morph", json=payload)
    assert res.status_code == 404

