def test_body_viewer_blocked(client, viewer_user, snapshot):
    res = client.post("/mutations/body/apply-morph", json={
        "project_id": snapshot.project_id,
        "base_snapshot_id": snapshot.id,
        "preset_id": "widebody_v1",
        "parameters": {}
    }, user=viewer_user)

    assert res.status_code == 403

