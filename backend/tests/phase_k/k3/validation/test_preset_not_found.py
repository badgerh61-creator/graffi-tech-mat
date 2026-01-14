def test_body_preset_not_found(client, admin_user, snapshot):
    payload = {
        "project_id": snapshot.project_id,
        "base_snapshot_id": snapshot.id,
        "preset_id": "nonexistent",
        "parameters": {}
    }

    res = client.post("/mutations/body/apply-morph", json=payload, user=admin_user)
    assert res.status_code == 404

