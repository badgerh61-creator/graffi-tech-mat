def test_body_parameters_out_of_bounds(client, completed_snapshot, admin_user):
    payload = {
        "project_id": completed_snapshot.project_id,
        "base_snapshot_id": completed_snapshot.id,
        "preset_id": "widebody_v1",
        "parameters": {"width_factor": 999},
    }

    res = client.post("/mutations/body/apply-morph", json=payload)
    assert res.status_code == 400

