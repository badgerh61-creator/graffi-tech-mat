def test_body_preset_incompatible(client, completed_snapshot, admin_user):
    payload = {
        "project_id": completed_snapshot.project_id,
        "base_snapshot_id": completed_snapshot.id,
        "preset_id": "truck_only_widebody",
        "parameters": {},
    }

    res = client.post("/mutations/body/apply-morph", json=payload)
    assert res.status_code == 409

