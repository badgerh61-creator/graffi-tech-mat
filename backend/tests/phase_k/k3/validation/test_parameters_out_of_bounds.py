def test_body_parameters_out_of_bounds(client, admin_user, snapshot):
    payload = {
        "project_id": snapshot.project_id,
        "base_snapshot_id": snapshot.id,
        "preset_id": "widebody_v1",
        "parameters": {"width_factor": 99}
    }

    res = client.post("/mutations/body/apply-morph", json=payload, user=admin_user)
    assert res.status_code == 400

